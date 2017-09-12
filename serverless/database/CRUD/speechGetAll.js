'use strict';
const TableName = require('../config').SpeechTable;
const getAll = require('./getAll');

const getAllSpeeches = (options = {}) => {
  return getAll(TableName, options);
};

module.exports = getAllSpeeches;