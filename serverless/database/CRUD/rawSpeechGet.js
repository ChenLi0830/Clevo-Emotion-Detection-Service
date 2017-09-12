/**
 * Created by Chen on 2017-07-29.
 */
'use strict';

const TableName = require('../config').RawSpeechTable;
const get = require('./get');

const getRawSpeech = (fileName) => {
  return get(TableName, {fileName});
};

module.exports = getRawSpeech;