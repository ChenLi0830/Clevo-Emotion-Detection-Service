'use strict';

const options = require('../config').options;
const calcFormEncode = require('./api').calcFormEncode;
const fetch = require('isomorphic-fetch');
const fs = require('fs');

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

const analyzeFile = (apiKey, token, content, fileName) => {
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
        console.log("data", data);
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
              console.log("response", response);
              return response.json();
            })
            .then(result => {
              return console.log("result", JSON.stringify(result))
            })
        // recordingId = result.recordingId;
      })
      .catch(err => {
        console.log("err", err);
      })
};

(async ()=>{
  let token = await getToken(options.apiKey, options);
  console.log("token", token);
  
  let file = fs.readFileSync('./20170623100908_861_13817033084_601.wav');
  // console.log("file", file);
  
  analyzeFile(options.apiKey, token, file, "20170623100908_861_13817033084_601.wav")
})();