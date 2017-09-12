'use strict';
let AWS = require('../config').AWS;
let docClient = new AWS.DynamoDB.DocumentClient();
const api = require('../api');

/**
 * Query Item from Index
 * @param {string} tableName
 * @param {string} indexName
 * @param {object} key - the key that corresponds to the item, for example, {restaurantId: "xxxx", stampedAt: "yyyy"}
 * @param {object} [options]
 * */

const queryByIndex = (tableName, indexName, key, options={}) => {
  // const {AttributesToGet=null, ConsistentRead=false} = options;
  
  // Get Query parameters
  const KeyConditionExpression = api.getKeyConditionExpression(key);
  const ExpressionAttributeValues = api.getExpressionAttributeValues(key);
  // console.log("KeyConditionExpression", KeyConditionExpression);
  // console.log("ExpressionAttributeValues", ExpressionAttributeValues);
  
  
  let params = {
    TableName: tableName,
    IndexName: indexName,
    KeyConditionExpression,
    ExpressionAttributeValues,
  };
  
  return new Promise((resolve, reject) => {
    docClient.query(params, function(err, data) {
      if (err) {
        console.error(`Unable to query item(s) from ${indexName} of ${tableName}. Error JSON:`, JSON.stringify(err), err.stack);
        return reject(err);
      }
      console.log(`Successfully queried ${data.Count} item(s) from ${tableName}, ${data.ScannedCount} items were scanned in total`);
      // console.log("data.Items", data.Items);
      resolve(data.Items);
      // else callback(null, data);
    });
  });
};

module.exports = queryByIndex;