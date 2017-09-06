let ffmpeg = require('fluent-ffmpeg');
let path = require('path');
let fs = require('fs');

// let filePath = 'https://s3-us-west-2.amazonaws.com/clevo.dev.recordings.companies/umf/20170623165732_642_18608122306_601.mp3';
// let filePath = '/Users/Chen/Downloads/yonel/data/wav/334485_211_084904.wav';

const convertAudioToWav = (filePath, outputPath = "./") => {
  let extension = path.extname(filePath);
  let baseName = path.basename(filePath, extension);
  
  if (extension!== ".mp3" && extension!== ".wav") {
    throw new Error(`extension ${extension} is not recognized!`);
  }
  
  return new Promise((resolve, reject)=>{
    ffmpeg(filePath)
        .toFormat('wav')
        .on('error', function (err) {
          console.log('An error occurred: ' + err.message);
          reject(err);
        })
        .on('progress', function (progress) {
          // console.log(JSON.stringify(progress));
          console.log('Processing: ' + progress.targetSize + ' KB converted');
        })
        .on('end', function () {
          console.log('Processing finished !');
          resolve();
        })
        .save(`${outputPath}${baseName}.wav`);//path where you want to save your file
  })
};

module.exports = convertAudioToWav;

// let extension = path.extname(filePath);
// let baseName = path.basename(filePath, extension);

