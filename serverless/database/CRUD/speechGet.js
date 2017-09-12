/**
 * Created by Chen on 2017-07-29.
 */
'use strict';
const TableName = require('../config').SpeechTable;
const get = require('./get');

const getSpeech = (fileName, operatorId) => {
  return get(TableName, {fileName, operatorId});
};

module.exports = getSpeech;