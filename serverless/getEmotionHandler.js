'use strict';
// let ffmpeg = require('fluent-ffmpeg');
// const path = require('path');
// const s3Root = "https://s3-us-west-2.amazonaws.com";
const AWS = require('aws-sdk');
const s3 = new AWS.S3();

const options = require('./config').options;
const calcFormEncode = require('./api').calcFormEncode;
const fetch = require('isomorphic-fetch');
const fs = require('fs');

const processedSpeechUpdate = require('./database/CRUD/processedSpeechUpdate');
const processedSpeechCreate = require('./database/CRUD/processedSpeechCreate');

const getToken = (apiKey, options) => {
  return fetch(options.url.tokenUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: calcFormEncode({
      "grant_type": "client_credentials",
      "apiKey": apiKey
    }),
  })
      .then((response) => response.json())
      .then(result => {
        // console.log("get token result", result);
        return result.access_token;
      })
};

const analyzeFile = (apiKey, token, content) => {
  return fetch(options.url.serverUrl + "start", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': "Bearer " + token,
    },
    body: '{"dataFormat":{"type":"WAV"}, "metadata": {"clientId": "someUser123@gmail.com"}, "displayLang":"zh-cn"}',
  })
      .then((response) => response.json())
      .then((data) => {
        // console.log("data", data);
        const recID = data.recordingId ? data.recordingId : JSON.parse(data).recordingId;
        const upStreamUrl = options.url.serverUrl + recID;
        
        return fetch(upStreamUrl, {
          method: 'POST',
          headers: {
            'Authorization': "Bearer " + token,
          },
          body: content,
        })
            .then(response => {
              // console.log("response", response);
              return response.json();
            })
            .then(result => {
              return result;
            })
        // recordingId = result.recordingId;
      })
      .catch(err => {
        console.log("err", err);
      })
};


module.exports.handler = (event, context, callback) => {
  console.log("event", JSON.stringify(event));
  console.log("context", JSON.stringify(context));
  
  // let records = event.Records;
  if (event.Records.length === 0) {
    return callback(new Error("no record"));
  }
  
  let method = "MODIFY";
  if (event.Records[0].eventName!==method || !event.Records[0].dynamodb){
    return callback(new Error(`Only method ${method} in dynamoDB is needed here`));
  }
  
  const image = event.Records[0].dynamodb.NewImage;
  if (!image){
    return callback(new Error(`no new image`));
  }
  
  const fileName = image.fileName.S;
  const fileExtension = image.fileExtension.S;
  
  console.log("trying to get record", `UMF/${fileName}.${fileExtension}`);
  
  if (image){
    s3.getObject({
      Bucket: "clevo.recordings.companies",
      Key: `UMF/${fileName}.${fileExtension}`,
    }, function(err, s3File) {
      if (err) {
        console.log(err, err.stack);
        const response = {
          statusCode: 404,
          body: JSON.stringify({
            message: JSON.stringify(err),
          }),
        };
  
        callback(null, response);
      } else {
  
        return getToken(options.apiKey, options)
            .then(token => {
              console.log("token", token);
  
              // let file = fs.readFileSync('./20170623100908_861_13817033084_601.wav');
              // console.log("file", file);
  
              return analyzeFile(options.apiKey, token, s3File.Body);
            })
            .then(result => {
              console.log("emotion result",  JSON.stringify(result));
              console.log("result.status",  JSON.stringify(result.status));
              console.log("result.result",  JSON.stringify(result.result));
              console.log("result.result.analysisSegments",  JSON.stringify(result.result.analysisSegments));
              if (result.status !== "success"){
                return callback(new Error(`get emotion result failed, response: ${JSON.stringify(result)}`));
              }
              
              return processedSpeechUpdate(fileName, {emotions: result.result.analysisSegments, duration: result.result.duration});
              // return processedSpeechUpdate(fileName, {emotions: result.result.analysisSegments, duration: result.result.duration});
            })
            .then(result => {
              //Todo 添加result到processed data
              
              const response = {
                statusCode: 200,
                body: JSON.stringify({
                  // message: 'Go Serverless v1.0! Your function executed successfully!',
                  // input: event,
                }),
              };
  
              callback(null, response);
            })
            .catch(error => {
              console.log("error", error);
              callback(error);
            })
      }
    });
  }
  
  
  


  // Use this code if you don't use the http event with the LAMBDA-PROXY integration
  // callback(null, { message: 'Go Serverless v1.0! Your function executed successfully!', event });
};
