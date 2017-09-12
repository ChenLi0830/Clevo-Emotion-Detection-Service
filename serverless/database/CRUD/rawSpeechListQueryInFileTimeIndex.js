const tableName = require('../config').RawSpeechTable;
const queryByIndex = require('./queryByIndex');
const indexName = require('../config').RawSpeechIndexFileTime;

const rawSpeechListQueryInTaskIdIndex = (fileName, transcribedAt) => {
  return queryByIndex(tableName, indexName, {fileName, transcribedAt});
};

module.exports = rawSpeechListQueryInTaskIdIndex;
