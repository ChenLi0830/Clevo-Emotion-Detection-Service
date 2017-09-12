// const getEmployeeId = (fileName) => {
//   return fileName.split('_')[1];
// };
//
// let result = getEmployeeId("20170623134952_966_02488089012_601");
//
// console.log(result);




let transcriptionList = JSON.parse("[{\"bg\":\"0\",\"ed\":\"4160\",\"onebest\":\"您好，966位服务，请问有什么能够帮助您的吗？\",\"speaker\":\"1\"},{\"bg\":\"4270\",\"ed\":\"10700\",\"onebest\":\"唉你好，我想你用那个号注册那个IP会员，现在怎么开通不了？啊。\",\"speaker\":\"2\"},{\"bg\":\"11310\",\"ed\":\"14910\",\"onebest\":\"您是用来电的这个手机号13\",\"speaker\":\"1\"},{\"bg\":\"15000\",\"ed\":\"16820\",\"onebest\":\"啊1519\",\"speaker\":\"1\"},{\"bg\":\"17090\",\"ed\":\"23720\",\"onebest\":\"9361是719吗？您稍等帮您查询。\",\"speaker\":\"1\"},{\"bg\":\"24770\",\"ed\":\"26290\",\"onebest\":\"你就拿我们的好\",\"speaker\":\"2\"},{\"bg\":\"26780\",\"ed\":\"27870\",\"onebest\":\"古城\",\"speaker\":\"2\"},{\"bg\":\"29570\",\"ed\":\"31280\",\"onebest\":\"我都你了。\",\"speaker\":\"2\"},{\"bg\":\"31410\",\"ed\":\"61400\",\"onebest\":\"您好！感谢您耐心等待查看到您是这个是因为话费余额不足，玩没有完成支付您上您可以查询一下您这个嗯可能您查询您打1086查询一下，可用于支付的话费是多少，可能最后有可能余额它这个不同吗？噢是的。因为那个他这个事比如说您积分兑换的这种话费就是不能用于支付类的。\",\"speaker\":\"1\"},{\"bg\":\"62510\",\"ed\":\"66950\",\"onebest\":\"啊但是我这余额就可以，但是我给他这些事情。\",\"speaker\":\"2\"},{\"bg\":\"66960\",\"ed\":\"70830\",\"onebest\":\"您稍等，我帮您查询一下您这个是甘肃的是吗？\",\"speaker\":\"1\"},{\"bg\":\"70850\",\"ed\":\"74200\",\"onebest\":\"啊对对对是的，等一下了\",\"speaker\":\"1\"},{\"bg\":\"74220\",\"ed\":\"77860\",\"onebest\":\"那个就是他完全可以玩，\",\"speaker\":\"1\"},{\"bg\":\"78430\",\"ed\":\"107650\",\"onebest\":\"谁知您好先生，感谢耐心等待噢您支付之后，就是说您购买这个会员之后保底余额还必须留30必须，然后以后噢不客气，还有其他能帮你吗？感谢您来电，请稍后评价这些。\",\"speaker\":\"1\"}]");

const analyzeTalkDurations = (transcriptionList) => {
  let speaker1Duration = 0, speaker2Duration = 0;
  transcriptionList.forEach(transcript => {
    if (transcript.speaker === "1") speaker1Duration += (transcript.ed - transcript.bg);
    else speaker2Duration += (transcript.ed - transcript.bg);
  });
  let silenceDuration = transcriptionList[transcriptionList.length - 1].ed - speaker1Duration - speaker2Duration;
  return [speaker1Duration, speaker2Duration, silenceDuration];
};

let newFields = {};
//[newFields.silenceDuration, newFields.speaker1TalkDuration, newFields.speaker2TalkDuration]
[newFields.speaker1TalkDuration, newFields.speaker2TalkDuration, newFields.silenceDuration] = analyzeTalkDurations(transcriptionList);

console.log("newFields", newFields);

