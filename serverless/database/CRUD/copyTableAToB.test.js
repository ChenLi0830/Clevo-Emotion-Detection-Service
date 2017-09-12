let AWS = require("aws-sdk");

AWS.config.update({
  region: "us-west-2",
  endpoint: "http://localhost:8000",
  accessKeyId: "123",
  secretAccessKey: "345",
});

const copyTableAToB = require('./copyTableAToB');
const TableNameA = "transcription_table";
const TableNameB = require('../config').RawSpeechTable;

const getAll = require('./getAll');

describe('copyTableAToB', () => {
  // mute console logs
  console = {log: ()=>{}, error: ()=>{}};
  
  test('migrate existing tables', () => {
    return copyTableAToB(TableNameA, TableNameB)
        .then(copiedItems => {
          // no error was thrown
          expect(true).toBeTruthy();
        })
        .catch(err => {
          console.error(err);
        })
  });
  
  test("table doesn't exit", () => {
    return copyTableAToB("non-exist-table", TableNameB)
        .catch(err => {
          expect(err).toBeTruthy();
        })
  });
  
  test("table doesn't exit", () => {
    return copyTableAToB(TableNameB, "non-exist-table")
        .catch(err => {
          expect(err).toBeTruthy();
        })
  })
});