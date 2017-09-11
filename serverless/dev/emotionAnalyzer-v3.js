var request = require('request')
var extend = require('extend')
var fs = require('fs');


var defaults = {
  tokenUrl: 'https://token.beyondverbal.com/token',
  serverUrl: 'https://apiv4.beyondverbal.com/v3/recording/',
  //use interval for stream analysis
  //interval:1000
}


//
// //Usage example
// var fs = require('fs')
// var Analyzer = require('./analyzer-v3')
//
//
// var analyzer = new Analyzer('YOUR_API_KEY')
//
// analyzer.analyze(fs.createReadStream('C:/path/to/Sample.wav'),function(err,analysis){
//     console.log(analysis);
//
// });
function Analyzer(apiKey, opts) {
  
  var tokenCahced = null;
  var options = extend({}, defaults, opts);
  this.analyze = function (stream, callback) {
    
    if (!tokenCahced) {
      return getToken(apiKey, options, function (err, token) {
        tokenCahced = token;
        console.log("tokenCahced", tokenCahced);
        return analyzeFile(tokenCahced, stream, options, callback);
      });
    }
    
    return analyzeFile(tokenCahced, stream, options, callback);
  }
  return;
}


module.exports = Analyzer;


///
/// options.apiKey
///
function getToken(apiKey, options, callback) {
  return request.post(options.tokenUrl, {
    form: {
      grant_type: "client_credentials",
      apiKey: apiKey
    }
  }, function (err, resp, body) {
    if (!err) {
      return callback(null, JSON.parse(body).access_token);
    } else {
      return callback(err);
    }
  });
}

function analyzeFile(token, stream, options, callback) {
  var startUrl = options.serverUrl + "start";
  var interval = options.interval;
  var streaming = interval;

  //1. start
  return request.post(startUrl, {
    json: true,
    body: { dataFormat: { type: "WAV" } },
    auth: { 'bearer': token }
  }, function (err, resp, body) {

    var timer;
    function errorCalback(err) {
      if (timer) { clearInterval(timer); }
      console.log(err.stack);
      callback(err);
    }

    if (err) {
      console.log(err.stack);
      return errorCalback(err);
    }

    var recordingUrl = options.serverUrl + body.recordingId;
    console.log("recordingUrl", recordingUrl);
    // console.log("resp", resp);
    // var wstream = fs.createWriteStream('./test.wav');
    // stream.pipe(wstream);
    stream.pipe(request.post(recordingUrl, { auth: { 'bearer': token } },
        function (err, resp, body) {
          if (err) {
            console.log(err, err.stack);
            errorCalback(err);
          } else {
            // if (!streaming) {
            var jsonResp = JSON.parse(body)
            callback(null, jsonResp);
            // }
          }
        }));

    return;
  });
}


// function analyzeFile(token, stream, options, callback) {
//   var startUrl = options.serverUrl + "start";
//   var interval = options.interval;
//   var streaming = interval;
//
//   //1. start
//   return request.post(startUrl, {
//     json: true,
//     body: { dataFormat: { type: "WAV" } },
//     auth: { 'bearer': token }
//   }, function (err, resp, body) {
//
//     var timer;
//     function errorCalback(err) {
//       if (timer) { clearInterval(timer); }
//       console.log(err.stack);
//       callback(err);
//     }
//
//     if (err) {
//       console.log(err.stack);
//       return errorCalback(err);
//     }
//
//     var recordingUrl = options.serverUrl + body.recordingId;
//     console.log("recordingUrl", recordingUrl);
//     // console.log("resp", resp);
//     // var wstream = fs.createWriteStream('./test.wav');
//     // stream.pipe(wstream);
//     stream.pipe(request.post(recordingUrl, { auth: { 'bearer': token } },
//         function (err, resp, body) {
//           if (err) {
//             console.log(err, err.stack);
//             errorCalback(err);
//           } else {
//             // if (!streaming) {
//             var jsonResp = JSON.parse(body)
//             callback(null, jsonResp);
//             // }
//           }
//         }));
//
//     if (streaming) {
//       var offset = 0;
//       timer = setInterval(function () {
//         console.log("if (streaming) {");
//         var analysisUrl = recordingUrl + "/analysis?fromMs=" + offset;
//         return request.get(analysisUrl, { auth: { 'bearer': token } }, function (err, resp, body) {
//           if (err) { console.log(err.stack); return errorCalback(err); }
//           else {
//             var jsonResp = JSON.parse(body),
//                 sessionStatus = jsonResp.result.sessionStatus;
//             if (sessionStatus === "Processing") {
//
//               if (jsonResp.result.analysisSegments) {
//                 //calculate and update ooset
//                 var len = jsonResp.result.analysisSegments.length - 1;
//                 offset = jsonResp.result.analysisSegments[len].offset;
//                 callback(null, jsonResp.result);
//               }
//
//             } else if (sessionStatus === "Done") {
//               if (timer) {
//                 clearInterval(timer);
//               }
//               callback(null, jsonResp.result);
//             }
//           }
//         })
//       }, interval);
//     }
//     return;
//   });
// }
