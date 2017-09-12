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

const processedSpeechUpdate = require('./database').processedSpeechUpdate;

const aggregateTranscriptions = (transcriptionList) => {
  let text = transcriptionList.reduce((aggregateResult, transcription) => aggregateResult+transcription.onebest, "");
  return text;
};

const callNLPMethod = (inputTxt, url)=>{
  let params = {text: inputTxt};
  const searchParams = Object.keys(params).map((key) => {
    return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
  }).join('&');
  
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    },
    body: searchParams
  })
      .then((response) => response.text())
      .then(result => {
        return result;
      });
};

const getSpeechCategorization = (aggregatedTranscription) => {
  return callNLPMethod(aggregatedTranscription, "https://clevo-categorize.appspot.com/");
};

const getSentenseCategorization = (transcription) => {
  return new Promise((resolve, reject)=>{
    return resolve(["扣款查询", "回答问题"]);
  })
  // return callNLPMethod(transcription, "https://clevo-categorize.appspot.com/")
};

module.exports.handler = (event, context, callback) => {
  console.log("event", JSON.stringify(event));
  
  // let records = event.Records;
  if (event.Records.length === 0) {
    console.log(new Error("no record"));
    return callback();
  }
  
  //Iterate over all records
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
  
      let transcriptionList = JSON.parse(newImage.transcriptionText.S);
      let speechTranscription = aggregateTranscriptions(transcriptionList);
      const fileName = newImage.fileName.S;
      
      //nlp promises 包括两部分，对整段话getSpeechCategorization和对每句话getSentenseCategorization
      let nlpPromises = [];
      nlpPromises.push(getSpeechCategorization(speechTranscription));
      
      transcriptionList.forEach(transcription => {
        let singleSentensePromise = getSentenseCategorization(transcription.onebest)
            .then(category => {
              return {
                bg: transcription.bg,
                ed: transcription.ed,
                onebest: transcription.onebest,
                speaker: transcription.speaker,
                categories: category
              }
            });
        
        nlpPromises.push(singleSentensePromise)
      });
      
      return Promise.all(nlpPromises)
          .then(results => {
            let newFields = {};
            newFields.categorizedSpeechTopic = results[0];
            console.log("categorizedSpeechTopic", categorizedSpeechTopic);
            newFields.categorizeResult = results.slice(1);
            console.log("categorizeResult", categorizeResult);
            return processedSpeechUpdate(fileName, newFields);
          })
      
      // return getSpeechCategorization(speechTranscription)
      //     .then(speechTopic => {
      //       console.log("businessCateResult", speechTopic);
      //
      //       //save speech topic to processed data
      //       processedSpeechNewFields.categorizedSpeechTopic = speechTopic;
      //       return speechTopic;
      //     })
      //     .then(speechTopic => {
      //
      //     })
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

};
