'use strict';
const TableName = require('../config').SentenceTable;
const getAll = require('./getAll');

const getAllSentences = (options = {}) => {
  return getAll(TableName, options);
};

module.exports = getAllSentences;