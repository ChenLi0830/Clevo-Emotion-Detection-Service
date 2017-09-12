/**
 * Created by Chen on 2017-07-29.
 */
'use strict';

const TableName = require('../config').RawSpeechTable;
const getAll = require('./getAll');

const getAllRawSpeech = (options = {}) => {
  return getAll(TableName, options);
};

module.exports = getAllRawSpeech;