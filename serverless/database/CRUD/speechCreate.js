/**
 * Created by Chen on 2017-07-29.
 */
'use strict';
const create = require('./create');
const TableName = require('../config').SpeechTable;
const _ = require('lodash');
const api = require('../api');
const getSpeech = require('./speechGet');

const createSentence = (args) => {
  return getSpeech(args.fileName, args.operatorId)
  //Check for duplication
      .then(duplicate => {
        if (duplicate && duplicate.fileName) {
          // operator exist
          return Promise.reject(new Error("Speech with same fileName and operatorId already exist"));
        }
        args.id = args.fileName + args.operatorId;
        return create(TableName, args);
      })
};

module.exports = createSentence;