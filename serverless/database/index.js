'use strict';

const speechGet = require('./CRUD/speechGet');
const speechCreate = require('./CRUD/speechCreate');
const speechGetAll = require('./CRUD/speechGetAll');

const sentenceCreate = require('./CRUD/sentenceCreate');
const sentenceGet = require('./CRUD/sentenceGet');
const sentenceGetAll = require('./CRUD/sentenceGetAll');

const rawSpeechCreate = require('./CRUD/rawSpeechCreate');
const rawSpeechGet = require('./CRUD/rawSpeechGet');
const rawSpeechGetAll = require('./CRUD/rawSpeechGetAll');
const rawSpeechUpdate = require('./CRUD/rawSpeechUpdate');
const rawSpeechListQueryInTaskIdIndex = require('./CRUD/rawSpeechListQueryInTaskIdIndex');
const rawSpeechListQueryInFileTimeIndex = require('./CRUD/rawSpeechListQueryInFileTimeIndex');

const processedSpeechUpdate = require('./CRUD/processedSpeechUpdate');
const processedSpeechCreate = require('./CRUD/processedSpeechCreate');

module.exports = {
  processedSpeechUpdate,
  processedSpeechCreate,
  rawSpeechGet
};