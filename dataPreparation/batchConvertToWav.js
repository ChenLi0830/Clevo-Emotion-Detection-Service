let ffmpeg = require('fluent-ffmpeg');
let path = require('path');
let fs = require('fs');
let _ = require('lodash');
const convertAudioToWav = require('./convertAudioToWav');
const readDirRecurs = require('./api').readDirRecurs;

// const dataFolderPath = '/Users/Chen/百度云同步盘/Startup/Clevo/联动数据/录音/';
// const outputPath = '/Users/Chen/百度云同步盘/Startup/Clevo/联动数据/wav/';
// let filePath = 'https://s3-us-west-2.amazonaws.com/clevo.dev.recordings.companies/umf/20170623165732_642_18608122306_601.mp3';
// let filePath = '/Users/Chen/Downloads/yonel/data/wav/334485_211_084904.wav';
const dataFolderPath = '/Users/Chen/百度云同步盘/Startup/Clevo/润华数据/';
const outputPath = '/Users/Chen/百度云同步盘/Startup/Clevo/润华数据/wav/';

if (!fs.existsSync(outputPath)) throw new Error("Output Path doesn't exist!");

let files = readDirRecurs(dataFolderPath);
console.log("files.length", files.length);
files = _.filter(files, file => path.extname(file)===".mp3" || path.extname(file)===".wav");

// console.log("files", files);
// console.log("files.length", files.length);

(async ()=>{
  // let counter = 0;
  for (let filePath of files){
    await convertAudioToWav(filePath, outputPath);
    // if (counter++ === 10) break;
  }
})();

