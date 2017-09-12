'use strict';
let AWS = require('../config').AWS;
let docClient = new AWS.DynamoDB.DocumentClient();
const api = require('../api');

/**
 * Update item in table
 * @param {string} tableName
 * @param {object} key - the key that corresponds to the item to be updated, for example, {restaurantId: "xxxx", stampedAt: "yyyy"}
 * @param {object} newFields - new fields to be updated, for example, {stampTotal: 5, cards: [{id:1, stampCount:2}, {id:2, stampCount:1}]}
 * @param {object} [options] update options, for example, {ReturnValues: "ALL_NEW"}
 * */
const update = (tableName, key, newFields, options = {}) => {
  const {ReturnValues = "ALL_NEW"} = options;
  // Check for argument errors
  if (!key) {
    return Promise.reject(new Error("Update fail: argument `key` is invalid"));
  }
  if (!newFields || Object.keys(newFields).length === 0) {
    return Promise.reject(new Error("Update fail: newFields can't be empty"));
  }
  
  // Get update parameters
  const UpdateExpression = api.getUpdateExpression(newFields);
  const ExpressionAttributeNames = api.getExpressionAttributeNames(newFields);
  const ExpressionAttributeValues = api.getExpressionAttributeValues(newFields);
  const timeStamp = api.getTimeInSec();
  
  let params = {
    TableName: tableName,
    Key: key,
    UpdateExpression,
    ExpressionAttributeNames,
    ExpressionAttributeValues,
    updatedAt:timeStamp,
    ReturnValues,
  };
  
  return new Promise((resolve, reject) => {
    docClient.update(params, (err, data) => {
      if (err) {
        console.error(`Unable to update in table ${tableName} for the following fields: ${JSON.stringify(newFields)}`,
            JSON.stringify(err), err.stack);
        return reject(err);
      } else {
        console.log(`Successfully updated item in ${tableName}`);
        resolve(data.Attributes);
      }
    });
  });
};

module.exports = update;