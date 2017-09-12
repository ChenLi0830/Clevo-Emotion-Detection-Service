'use strict';

let AWS = require("aws-sdk");

/**
 * For testing on local DynamoDB
 **/
console.log("process.env.DEBUG_MODE", process.env.DEBUG_MODE);
if (process.env.DEBUG_MODE) {
  AWS.config.update({
    region: "us-west-2",
    endpoint: "http://localhost:8000",
    accessKeyId: "123",
    secretAccessKey: "345",
  });
}

// const OperatorTable = "Clevo-Manual-Operators";
// const SpeechTable = "Clevo-Categorized-Speech-Table";
// const SentenceTable = "Clevo-Categorized-Sentence-Table";
// const RawSpeechTable = "Clevo-Raw-Speech-Table";
const ProcessedSpeechTable = "Clevo-Processed-Speech-Table";
// const RawSpeechTable = "transcription_table";

// const RawSpeechIndexTaskId = "xfTaskId-index";
// const RawSpeechIndexFileTime = "file-time-index";

module.exports = {
  ProcessedSpeechTable,
  AWS
};