'use strict';
let AWS = require('../config').AWS;
let docClient = new AWS.DynamoDB.DocumentClient();
const _ = require('lodash');
const api = require('../api');

/**
* Create Item in table, 'createdAt' and 'updatedAt' timeStamps will be added in each item
* */
const create = (tableName, item, options={}) => {
  const {ReturnValues = "NONE", ReturnConsumedCapacity="NONE"} = options;
  
  const timeStamp = api.getTimeInSec();
  
  item.createdAt = timeStamp;
  item.updatedAt = timeStamp;
  
  let params = {
    TableName: tableName,
    Item: item,
    ReturnConsumedCapacity: ReturnConsumedCapacity,
    ReturnValues: ReturnValues,
  };
  
  return new Promise((resolve, reject) => {
    docClient.put(params, (err, data) => {
      if (err) {
        console.error(`Unable to insert item into ${tableName}. Error JSON:`, JSON.stringify(err), err.stack);
        return reject(err);
      } else {
        console.log(`Successfully inserted item into table ${tableName}`);
        resolve(item);
      }
    });
  });
};

module.exports = create;