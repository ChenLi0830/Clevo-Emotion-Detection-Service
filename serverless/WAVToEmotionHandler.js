'use strict';

const options = require('./config').options;

// let options = {
//   url: {
//     tokenUrl: 'https://token.beyondverbal.com/token',
//     // serverUrl: 'https://apiv3.beyondverbal.com/v1/recording/'
//     serverUrl: 'https://apiv4.beyondverbal.com/v3/recording/',
//   },
//   apiKey: "4a34bb65-5bfd-4006-af26-64aa63055b8b",
//   token: ''
// };

module.exports.convertAudioToWAV = (event, context, callback) => {
  const response = {
    statusCode: 200,
    body: JSON.stringify({
      message: 'Go Serverless v1.0! Your function executed successfully!',
      input: event,
    }),
  };
  
  callback(null, response);
  
  // Use this code if you don't use the http event with the LAMBDA-PROXY integration
  // callback(null, { message: 'Go Serverless v1.0! Your function executed successfully!', event });
};




const analyzeFile = (apiKey, content, fileName) => {
  return fetch(options.url.serverUrl + "start", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': "Bearer " + props.token,
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
            'Authorization': "Bearer " + props.token,
          },
          body: content,
        })
            .then(response => {
              console.log("response", response);
              return response.json();
            })
            .then(result => {
              console.log("result", result);
              let recordList = [...props.data];
              let totalMoodValue21 = 0, totalMoodValue11 = 0, totalArousal = 0,
                  totalTemper = 0, totalMoodValue11P = 0, totalMoodValue21P = 0;
              
              for (let segment of result.result.analysisSegments) {
                const {analysis} = segment;
                const mood11 = analysis && analysis.Mood ? analysis.Mood.Group11 : {Primary:"", Secondary:""};
                const mood21 = analysis && analysis.Mood ? analysis.Mood.Group21 : {Primary:"", Secondary:""};
                
                let moodValue11 = weights11[mood11.Primary.Phrase] + weights11[mood11.Secondary.Phrase] * 0.75;
                let moodValue21 = weights21[mood21.Primary.Phrase] + weights21[mood21.Secondary.Phrase] * 0.75;
                
                totalMoodValue11 += isNaN(moodValue11) ? 0 : moodValue11;
                totalMoodValue21 += isNaN(moodValue21) ? 0 : moodValue21;
                totalMoodValue11P += isNaN(weights11[mood11.Primary.Phrase]) ? 0 : weights11[mood11.Primary.Phrase];
                totalMoodValue21P += isNaN(weights21[mood21.Primary.Phrase]) ? 0 : weights21[mood21.Primary.Phrase];
                
                totalArousal += Math.trunc(analysis.Arousal.Value > 0 ? analysis.Arousal.Value : 50);
                totalTemper += Math.trunc(analysis.Temper.Value > 0 ? analysis.Temper.Value : 50);
                
                let record = {
                  name: fileName,
                  time: `${Math.trunc(segment.offset / 1000)} - ${Math.trunc(
                      segment.end / 1000)}`,
                  arousal: `${analysis.Arousal.Value}: ${analysis.Arousal.Score}%`,
                  temper: `${analysis.Temper.Value}: ${analysis.Temper.Score}%`,
                  valence: `${analysis.Valence.Value}: ${analysis.Valence.Score}%`,
                  // group7: `${analysis.Mood.Group7.Primary.Phrase} /
                  // ${analysis.Mood.Group7.Secondary.Phrase}`,
                  group11: `${mood11EnToZh[mood11.Primary.Phrase]} / ${mood11EnToZh[mood11.Secondary.Phrase]} (${moodValue11})`,
                  group21: `${mood21EnToZh[mood21.Primary.Phrase]} / ${mood21EnToZh[mood21.Secondary.Phrase]} (${moodValue21})`,
                };
                recordList.push(record);
              }
              totalMoodValue11 /= result.result.analysisSegments.length;
              totalMoodValue21 /= result.result.analysisSegments.length;
              totalMoodValue11P /= result.result.analysisSegments.length;
              totalMoodValue21P /= result.result.analysisSegments.length;
              totalArousal /= result.result.analysisSegments.length;
              totalTemper /= result.result.analysisSegments.length;
              
              console.log("fileName", fileName, "totalMoodValue", totalMoodValue11, "totalMoodValue21", totalMoodValue21, "totalArousal", totalArousal, "totalTemper", totalTemper);
              props.updateData(recordList);
              
              // console.log("props.summaryList", props.summaryList);
              summaryList.push({
                name: fileName,
                time: Math.trunc(result.result.duration / 1000) + "s",
                arousal: parseFloat(totalArousal).toFixed(2),
                temper: parseFloat(totalTemper).toFixed(2),
                group11: parseFloat(totalMoodValue11).toFixed(2) + " / " + parseFloat(totalMoodValue11P).toFixed(2),
                group21: parseFloat(totalMoodValue21).toFixed(2) + " / " + parseFloat(totalMoodValue21P).toFixed(2),
              });
              
              // console.log("newSummaryList", newSummaryList);
              if (summaryList.length === props.fileList.length) {
                console.log("summaryList", summaryList);
                props.updateSummary(summaryList);
              }
            });
        // recordingId = result.recordingId;
      })
      .catch(err => {
        console.log("err", err);
      })
};