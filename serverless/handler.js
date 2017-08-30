'use strict';
// let ffmpeg = require('fluent-ffmpeg');
// const path = require('path');
// const s3Root = "https://s3-us-west-2.amazonaws.com";

module.exports.convertAudioToWAV = (event, context, callback) => {

  let fluentFfmpeg = require('fluent-ffmpeg');
  let path = require('path');
  let filePath = 'https://s3-us-west-2.amazonaws.com/clevo.dev.recordings.companies/umf/20170623165732_642_18608122306_601.mp3';

  let extension = path.extname(filePath);
  let baseName = path.basename(filePath, extension);

  console.log("extension", extension, "baseName", baseName);

  if (extension === ".mp3"){
    fluentFfmpeg(filePath)
        .toFormat('wav')
        .on('error', function (err) {
          console.log('An error occurred: ' + err.message);
        })
        .on('progress', function (progress) {
          // console.log(JSON.stringify(progress));
          console.log('Processing: ' + progress.targetSize + ' KB converted');
        })
        .on('end', function () {
          console.log('Processing finished !');
        })
        .save(`./${baseName}.wav`);//path where you want to save your file
  }

  // console.log("event", JSON.stringify(event));
  //
  // event.Records.forEach((record) => {
  //   let bucketName = record.s3.bucket.name;
  //   let filePath = record.s3.object.key;
  //   let URL = `${s3Root}/${bucketName}/${filePath}`;
  //
  //   console.log("URL", URL);
  //
  //   let extension = path.extname(filePath);
  //   let baseName = path.basename(filePath, extension);
  //
  //   console.log("extension", extension, "baseName", baseName);
  //
  //   if (extension === ".mp3"){
  //     console.log(`Converting audio from .mp3 ${URL} to .wav`);
  //     ffmpeg(URL)
  //         .toFormat('wav')
  //         .on('error', function (err) {
  //           console.log('An error occurred: ' + err.message);
  //         })
  //         .on('progress', function (progress) {
  //           // console.log(JSON.stringify(progress));
  //           console.log('Processing: ' + progress.targetSize + ' KB converted');
  //         })
  //         .on('end', function () {
  //           console.log('Processing finished !');
  //         })
  //     .save(`'/tmp/${baseName}.wav`);//path where you want to save your file
  //   }
  //
  // });
  
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
