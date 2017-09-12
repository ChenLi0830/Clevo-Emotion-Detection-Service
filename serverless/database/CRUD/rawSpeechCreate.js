'use strict';
const create = require('./create');
const TableName = require('../config').RawSpeechTable;
const _ = require('lodash');
const api = require('../api');
const getRawSpeech = require('./rawSpeechGet');

const createRawSpeech = (args) => {
  return getRawSpeech(args.fileName)
  //Check for duplication
      .then(duplicate => {
        if (duplicate && duplicate.fileName) {
          // operator exist
          return Promise.reject(new Error("Raw speech with same fileName already exist"));
        }
        
        args.id = args.fileName;
        return create(TableName, args);
      })
};

module.exports = createRawSpeech;