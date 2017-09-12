/**
 * Created by Chen on 2017-07-29.
 */
'use strict';

//更新，添加 categorized count
const TableName = require('../config').RawSpeechTable;
const update = require('./update');

const updateRawSpeech = (fileName, newFields, options = {}) => {
  return update(TableName, {fileName}, newFields, options)
};

module.exports = updateRawSpeech;