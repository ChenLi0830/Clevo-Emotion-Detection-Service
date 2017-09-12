'use strict';
let AWS = require('../config').AWS;
let docClient = new AWS.DynamoDB.DocumentClient();
const api = require('../api');
const getAll = require('./getAll');
const update = require('./update');

/**
 * Update fields for all items in a table, use this when new fields are added to pre-existed table
 * @param {string} tableName
 * @param {object} keyNameArray - the key of the table, for example, ["restaurantId", "stampedAt"], or ["id"]
 * @param {object} newFields - new fields to be updated, for example, {stampTotal: 5, cards: [{id:1, stampCount:2}, {id:2, stampCount:1}]}
 * @param {boolean} forceUpdate - whether to force updated the field. In case of false, the field it will only be updated if it is null. If true, the field will always be updated.
 * @param {object} [options] update options, for example, {ReturnValues: "ALL_NEW"}
 * */
const updateAll = (tableName, keyNameArray, newFields, forceUpdate=false, options = {}) => {
  // Check for argument errors
  if (!keyNameArray || keyNameArray.length === 0) {
    return Promise.reject(new Error("Update fail: argument `keyNameArray` is invalid"));
  }
  if (!newFields || Object.keys(newFields).length === 0) {
    return Promise.reject(new Error("Update fail: newFields can't be empty"));
  }
  
  return getAll(tableName)
      // update all records
      .then(allItems => {
        let updateCount = allItems.length;
        console.log(`Update all items for fields ${JSON.stringify(newFields)}`);
        
        let promises = allItems.map(item => {
          let newFieldsOfItem = Object.assign({}, newFields);
          if (!forceUpdate){
            for (let field of Object.keys(newFieldsOfItem)){
              if (item[field]) {//remove field if it already exist
                // console.log(`item already has field ${field}`);
                delete newFieldsOfItem[field];
              }
            }
          }
  
          //if newFieldsOfItem is empty, skip this update
          if (Object.keys(newFieldsOfItem).length === 0) {
            updateCount--;
            return Promise.resolve();
          }
          
          //get the Key of item (partition key and sort key)
          let itemKey = {};
          for (let keyName of keyNameArray){
            itemKey[keyName] = item[keyName];
          }
  
          return update(tableName, itemKey, newFieldsOfItem, options)
        });
        
        return Promise.all(promises)
            .then(result => {
              console.log(`There are ${allItems.length} items in the table, and ${updateCount} items were updated`);
              return result;
            })
      });
};

module.exports = updateAll;