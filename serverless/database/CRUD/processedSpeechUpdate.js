'use strict';
const TableName = require('../config').ProcessedSpeechTable;
const update = require('./update');

const updateProcessedSpeech = (fileName, newFields, options = {}) => {
  return update(TableName, {fileName}, newFields, options)
};

module.exports = updateProcessedSpeech;