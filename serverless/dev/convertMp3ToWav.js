let ffmpeg = require('fluent-ffmpeg');
let path = require('path');
let filePath = 'https://s3-us-west-2.amazonaws.com/clevo.dev.recordings.companies/umf/20170623165732_642_18608122306_601.mp3';

let extension = path.extname(filePath);
let baseName = path.basename(filePath, extension);

console.log("extension", extension, "baseName", baseName);

if (extension === ".mp3"){
  ffmpeg(filePath)
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
