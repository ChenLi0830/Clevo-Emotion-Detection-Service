var fs = require('fs')
var Analyzer = require('./emotionAnalyzer-v3')
const fetch = require('isomorphic-fetch');
let token = '4a34bb65-5bfd-4006-af26-64aa63055b8b';

var analyzer = new Analyzer(token);

const stream = fs.createReadStream('./20170623100908_861_13817033084_601.wav');

// console.log("stream", stream);

// analyzer.analyze(stream,function(err,analysis){
//   console.log("reached analyzer.analyze(fs.createReadStream");
//   console.log(analysis);
// });


stream.on('data', function (chunk) {
  console.log("chunk", chunk);
  // const upStreamUrl = "https://apiv4.beyondverbal.com/v3/recording/" + recID;
  const upStreamUrl = "https://apiv4.beyondverbal.com/v3/recording/e5be1dc8-71c9-4a6a-85e3-bc1fad13cf16";

  return fetch(upStreamUrl, {
    method: 'POST',
    headers: {
      'Authorization': "Bearer " + token,
    },
    body: chunk,
  })
      .then(response => {
        console.log("response", response);
        return response.json();
      })
      .then(result => {
        return console.log("result", JSON.stringify(result))
      })
});
