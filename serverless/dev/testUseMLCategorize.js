const fetch = require('isomorphic-fetch');

// let text = "您好，966位服务，请问有什么能够帮助您的吗？唉你好，我想你用那个号注册那个IP会员，现在怎么开通不了？啊。您是用来电的这个手机号13啊1519936市郊是719是吗？您稍等帮您查一下。比如拿我们这套古城我都尽力了。您好！感谢您耐心等待查看到您是这个是因为话费余额不足，玩没有完成支付您上您可以查询一下您这个嗯可能您查询您打1086查询一下，可用于支付的话费是多少，可能最后有可能余额它这个不同吗？噢是的。因为那个他这个事比如说您积分兑换的这种话费就是不能用于支付类的。啊但是我这余额就会干扰我的事情。您稍等，我帮您查询一下您这个是甘肃的是吗？啊对对对是的，等一下了那个就是他完全可以玩，谁知您好先生，感谢耐心等待噢您支付之后，就是说您购买这个会员之后保底余额还必须留30必须，然后以后噢不客气，还有其他能帮你吗？感谢您来电，请稍后评价这些。";
// let url = "https://clevo-categorize.appspot.com/";
//
// const params = {text};
//
// const searchParams = Object.keys(params).map((key) => {
//   return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
// }).join('&');
//
// return fetch(url, {
//   method: 'POST',
//   headers: {
//     'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
//   },
//   body: searchParams
// })
//     .then((response) => response.text())
//     .then(result => {
//       return result;
//     });
const callNLPMethod = (inputTxt, url)=>{
  let params = {text: inputTxt};
  const searchParams = Object.keys(params).map((key) => {
    return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
  }).join('&');
  
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    },
    body: searchParams
  })
      .then((response) => response.text())
      .then(result => {
        return result;
      });
};

const getBusinessType = (aggregatedTranscription) => {
  return callNLPMethod(aggregatedTranscription, "https://clevo-categorize.appspot.com/");
};

getBusinessType("您好，966位服务，请问有什么能够帮助您的吗？唉你好，我想你用那个号注册那个IP会员，现在怎么开通不了？啊。您是用来电的这个手机号13啊1519936市郊是719是吗？您稍等帮您查一下。比如拿我们这套古城我都尽力了。您好！感谢您耐心等待查看到您是这个是因为话费余额不足，玩没有完成支付您上您可以查询一下您这个嗯可能您查询您打1086查询一下，可用于支付的话费是多少，可能最后有可能余额它这个不同吗？噢是的。因为那个他这个事比如说您积分兑换的这种话费就是不能用于支付类的。啊但是我这余额就会干扰我的事情。您稍等，我帮您查询一下您这个是甘肃的是吗？啊对对对是的，等一下了那个就是他完全可以玩，谁知您好先生，感谢耐心等待噢您支付之后，就是说您购买这个会员之后保底余额还必须留30必须，然后以后噢不客气，还有其他能帮你吗？感谢您来电，请稍后评价这些。")
    .then(result => {
      let businessCateResult = result;
      console.log("businessCateResult", businessCateResult);
    });
