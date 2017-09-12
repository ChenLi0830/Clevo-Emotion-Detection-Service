let path = require('path');
let fs = require('fs');

const readDirRecurs = (dir) =>
    fs.readdirSync(dir)
        .reduce((files, file) =>
                fs.statSync(path.join(dir, file)).isDirectory() ?
                    files.concat(readDirRecurs(path.join(dir, file))) :
                    files.concat(path.join(dir, file)),
            []);

const calcFormEncode = (properties) => {
  let formBody = [];
  for (let property in properties) {
    let encodedKey = encodeURIComponent(property);
    let encodedValue = encodeURIComponent(properties[property]);
    formBody.push(encodedKey + "=" + encodedValue);
  }
  formBody = formBody.join("&");
  return formBody;
};

const getEmotionScore = (analysisSegments, duration)=>{
  const weights11 = {
    "Creative, Passionate": 5,
    "Criticism, Cynicism": 1,
    "Defensivness, Anxiety": 2,
    "Friendly, Warm": 5,
    "Hostility, Anger": 1,
    "Leadership, Charisma": 4,
    "Loneliness, Unfulfillment": 3,
    "Love, Happiness": 5,
    "Sadness, Sorrow": 3,
    "Self-Control, Practicality": 3,
    "Supremacy, Arrogance": 1,
  };
  
  let totalToneScore = 0, totalEmoScore = 0, abnormalEmotions = [];
  
  analysisSegments.forEach(emotionSeg => {
    let segDuration = emotionSeg.duration;
    
    let mood11P = emotionSeg.analysis.Mood.Group11.Primary.Phrase;
    let mood11S = emotionSeg.analysis.Mood.Group11.Secondary.Phrase;
    
    let emoScore = (weights11[mood11P]*0.6 + weights11[mood11S]*0.4);
    totalEmoScore += emoScore * segDuration / duration;
    
    let positivity = emotionSeg.analysis.Valence.Value;
    let temper = emotionSeg.analysis.Temper.Value;
    let positivityGroup = emotionSeg.analysis.Valence.Group;
    let temperGroup = emotionSeg.analysis.Temper.Group;
    
    console.log("mood11P", mood11P,"mood11S", mood11S);
    console.log("positivity", positivity,"temper", temper);
    console.log("positivityGroup", positivityGroup, "temperGroup", temperGroup);
    
    if (positivityGroup==="negative" && temperGroup==="high" && emoScore ===1) {//Obvious bad emotion
      abnormalEmotions.push(emotionSeg);
    }
    
    let negativeScore = Math.abs(temper-50) - positivity; // 0~50 - 0~100 = -100~50，越大越不好
  
    totalToneScore+=negativeScore * segDuration / duration;
    
    console.log("emoScore", emoScore, "negativeScore", negativeScore);
  });
  
  console.log("totalEmoScore", totalEmoScore, "totalToneScore", totalToneScore, "abnormalEmotions", abnormalEmotions);
  return [totalEmoScore, totalToneScore, abnormalEmotions];
}

module.exports = {readDirRecurs, calcFormEncode, getEmotionScore};