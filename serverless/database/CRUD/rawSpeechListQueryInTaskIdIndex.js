const tableName = require('../config').RawSpeechTable;
const queryByIndex = require('./queryByIndex');
const indexName = require('../config').RawSpeechIndexTaskId;

const rawSpeechListQueryInTaskIdIndex = (xfTaskId) => {
  return queryByIndex(tableName, indexName, {xfTaskId});
};

module.exports = rawSpeechListQueryInTaskIdIndex;
