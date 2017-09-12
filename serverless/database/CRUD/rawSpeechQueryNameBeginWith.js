// /**
//  * Created by Chen on 2017-07-29.
//  */
// 'use strict';
//
// // const TableName = require('../config').RawSpeechTable;
// // const getAll = require('./getAll');
// //
// // const getAllRawSpeech = (options = {}) => {
// //   return getAll(TableName, options);
// // };
// //
// // const documentClient = new AWS.DynamoDB.DocumentClient();
// //
// // const params = {
// //   TableName: 'Table',
// //   IndexName: 'Index',
// //   KeyConditionExpression: 'HashKey = :hkey and RangeKey > :rkey',
// //   ExpressionAttributeValues: {
// //     ':hkey': 'key',
// //     ':rkey': 2015
// //   }
// // };
// //
// //
// //
// // documentClient.query(params, function(err, data) {
// //   if (err) console.log(err);
// //   else console.log(data);
// // });
//
// 'use strict';
// let AWS = require('../config').AWS;
// let docClient = new AWS.DynamoDB.DocumentClient();
//
// /**
//  * Query Item with hash key that begins with
//  * @param {string} tableName
//  * @param {object} key - the key that corresponds to the item, for example, {restaurantId: "xxxx", stampedAt: "yyyy"}
//  * @param {object} [options]
//  * */
// const get = (tableName, key, options={}) => {
//   const {AttributesToGet=null, ConsistentRead=false} = options;
//
//   const params = {
//     TableName: 'Table',
//     IndexName: 'Index',
//     KeyConditionExpression: 'HashKey = :hkey and RangeKey > :rkey',
//     ExpressionAttributeValues: {
//       ':hkey': 'key',
//       ':rkey': 2015
//     }
//   };
//
//   return new Promise((resolve, reject) => {
//     docClient.get(params, (err, data) => {
//       if (err) {
//         console.error(`Unable to get item from ${tableName}. Error JSON:`, JSON.stringify(err), err.stack);
//         return reject(err);
//       }
//       console.log(`Successfully get item from ${tableName}`);
//       resolve(data.Item);
//     });
//   });
// };
//
// // module.exports = get;
//
// module.exports = getAllRawSpeech;