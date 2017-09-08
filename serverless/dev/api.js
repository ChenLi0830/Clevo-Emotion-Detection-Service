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

module.exports = {readDirRecurs, calcFormEncode};