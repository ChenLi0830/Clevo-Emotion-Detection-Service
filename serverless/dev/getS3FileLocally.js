'use strict';
// let ffmpeg = require('fluent-ffmpeg');
// const path = require('path');
// const s3Root = "https://s3-us-west-2.amazonaws.com";
const AWS = require('aws-sdk');
const s3 = new AWS.S3();

// Use this to protect from accidentally apply this to production server
if (!process.env.PRODUCTION_MODE) {
  console.log("testing on local server");
  AWS.config.update({
    region: "us-west-2",
    endpoint: "http://localhost:8000",
    accessKeyId: "123",
    secretAccessKey: "345",
  });
} else {
  console.log("Applying changes on AWS server");
  AWS.config.update({
    region: "us-west-2",
  });
}

s3.getObject({
  Bucket: "clevo.recordings.companies",
  Key:"UMF/20170623124429_642_15245870466_601.mp3",
  // Key: "UMF/20170623124940_642_13941836605_601.mp3"
}, function(err, data) {
  if (err) {
    console.log(err, err.stack);
    // callback(err);
  } else {
    // console.log("Raw text:\n" + data.Body.toString('ascii'));
    console.log("data", data);
    // callback(null, null);
  }
});
