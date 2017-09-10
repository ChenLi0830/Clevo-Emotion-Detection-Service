'use strict';
// let ffmpeg = require('fluent-ffmpeg');
// const path = require('path');
// const s3Root = "https://s3-us-west-2.amazonaws.com";

module.exports.handler = (event, context, callback) => {
  console.log("event", event);
  console.log("context", context);
  
  const response = {
    statusCode: 200,
    body: JSON.stringify({
      // message: 'Go Serverless v1.0! Your function executed successfully!',
      // input: event,
    }),
  };
  
  callback(null, response);
  
  // Use this code if you don't use the http event with the LAMBDA-PROXY integration
  // callback(null, { message: 'Go Serverless v1.0! Your function executed successfully!', event });
};
