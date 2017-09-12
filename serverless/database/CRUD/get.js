'use strict';
let AWS = require('../config').AWS;
let docClient = new AWS.DynamoDB.DocumentClient();

/**
 * Get Item from table
 * @param {string} tableName
 * @param {object} key - the key that corresponds to the item, for example, {restaurantId: "xxxx", stampedAt: "yyyy"}
 * @param {object} [options]
 * */
const get = (tableName, key, options={}) => {
  const {AttributesToGet=null, ConsistentRead=false} = options;
  let params = {
    TableName: tableName,
    Key: key,
    AttributesToGet,
    ConsistentRead,
  };
  return new Promise((resolve, reject) => {
    docClient.get(params, (err, data) => {
      if (err) {
        console.error(`Unable to get item from ${tableName}. Error JSON:`, JSON.stringify(err), err.stack);
        return reject(err);
      }
      console.log(`Successfully get item from ${tableName}`);
      resolve(data.Item);
    });
  });
};

module.exports = get;