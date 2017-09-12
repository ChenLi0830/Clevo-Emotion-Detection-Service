'use strict';
let AWS = require('../config').AWS;
let docClient = new AWS.DynamoDB.DocumentClient();

/**
 * Get all items from table
 * @param {string} tableName
 * @param {object} [options] - scan options
 * @return {Promise.<Array.<*>>}
 * */
const getAll = (tableName, options={}) => {
  const {projectionExpression} = options;
  
  let ExpressionAttributeNames,
      newProjectionExpression;
  if (projectionExpression){
    ExpressionAttributeNames = {};
    for (let attributeName of projectionExpression.replace(/ /g,'').split(',')){
      ExpressionAttributeNames[`#${attributeName}`] = attributeName;
    }
    newProjectionExpression = Object.keys(ExpressionAttributeNames).join(',');
  }
  
  let params = {
    TableName: tableName,
    ProjectionExpression: newProjectionExpression,
    ExpressionAttributeNames,
  };
  
  return new Promise((resolve, reject) => {
    let result = [];
    
    const onScan = (err, data) => {
      if (err) {
        console.error(`Unable to get all items from ${tableName}. Error JSON:`, JSON.stringify(err), err.stack);
        return reject(err);
      }
      console.log("Object.keys(data)", Object.keys(data));
      
      result = result.concat(data.Items);
      
      // If there is more to scan, then scan again
      if (typeof data.LastEvaluatedKey != "undefined") {
        console.log("Scanning for more...");
        params.ExclusiveStartKey = data.LastEvaluatedKey;
        docClient.scan(params, onScan);
      } else {
        console.log(`Successfully get all ${result.length} items from ${tableName}`);
        resolve(result);
      }
    };
    
    docClient.scan(params, onScan);
  });
};

module.exports = getAll;