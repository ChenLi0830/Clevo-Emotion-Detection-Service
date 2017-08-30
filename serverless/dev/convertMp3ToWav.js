let ffmpeg = require('fluent-ffmpeg');
let path = require('path');
let track = 'https://s3-us-west-2.amazonaws.com/clevo.dev.recordings.companies/umf/20170623165732_642_18608122306_601.mp3';//your path to source file

let extension = path.extname(track);
let baseName = path.basename(track, extension);

console.log("extension", extension, "baseName", baseName);

if (extension === ".mp3"){
  ffmpeg(track)
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
