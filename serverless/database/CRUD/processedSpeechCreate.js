'use strict';
const TableName = require('../config').ProcessedSpeechTable;
const create = require('./create');

const createProcessedSpeech = (fileName, newFields, options = {}) => {
  console.log("newFields", newFields);
  return create(TableName, {fileName}, newFields, options)
};

module.exports = createProcessedSpeech;