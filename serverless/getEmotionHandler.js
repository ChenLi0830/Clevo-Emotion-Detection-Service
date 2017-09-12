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
const api = require('./api');

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
    console.log(new Error("no record"));
    return callback();
  }
  
  let promises = event.Records.map(record => {
    return new Promise((resolve, reject)=>{
      let method = "MODIFY";
      if ((record.eventName!==method/* && record.eventName!=="MODIFY"*/) || !record.dynamodb){
        console.log(new Error(`Method ${record.eventName} in dynamoDB is not needed here`));
        return reject();
      }
  
      const newImage = record.dynamodb.NewImage;
      const oldImage = record.dynamodb.OldImage;
      if (!newImage || !oldImage){
        console.log(new Error(`no new or old image`));
        return reject();
      }
      if (JSON.stringify(oldImage.transcriptionText) === JSON.stringify(newImage.transcriptionText)){
        console.log(new Error(`the modification is not in transcription`));
        return reject();
      }
  
      const fileName = newImage.fileName.S;
      const fileExtension = newImage.fileExtension.S;
  
      console.log("trying to get record", `UMF/${fileName}.${fileExtension}`);
  
      s3.getObject({
        Bucket: "clevo.recordings.companies",
        Key: `UMF/${fileName}.${fileExtension}`,
      }, function(err, s3File) {
        if (err) {
          console.log(err, err.stack);
          return reject()
        } else {
          return getToken(options.apiKey, options)
              .then(token => {
                console.log("token", token);
            
                return analyzeFile(options.apiKey, token, s3File.Body);
              })
              .then(result => {
                console.log("emotion result",  JSON.stringify(result));
                console.log("result.status",  JSON.stringify(result.status));
                console.log("result.result",  JSON.stringify(result.result));
                console.log("result.result.analysisSegments",  JSON.stringify(result.result.analysisSegments));
                if (result.status !== "success"){
                  console.log(new Error(`get emotion result failed, response: ${JSON.stringify(result)}`));
                  return reject();
                }
            
                let [totalEmoScore, totalToneScore, abnormalEmotions] = api.getEmotionScore(result.result.analysisSegments, result.result.duration);
            
                console.log("totalEmoScore, totalToneScore, abnormalEmotions", totalEmoScore, totalToneScore, abnormalEmotions);
            
                return processedSpeechUpdate(fileName, {emotions: result.result.analysisSegments, speechDuration: result.result.duration, totalEmoScore, totalToneScore, abnormalEmotions});
                // return processedSpeechUpdate(fileName, {emotions: result.result.analysisSegments, duration: result.result.duration});
              })
              .then(result => {
                //Todo 添加result到processed data
                return resolve(result);
              })
              .catch(error => {
                console.log("error", error);
                return reject(error);
              })
          }
        });
    })
  });
  
  return Promise.all(promises)
      .then(results => {
        console.log("promise results", results);
        
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
        callback();
      })

  // Use this code if you don't use the http event with the LAMBDA-PROXY integration
  // callback(null, { message: 'Go Serverless v1.0! Your function executed successfully!', event });
};
