let path = require('path');
let fs = require('fs');

const readDirRecurs = (dir) =>
    fs.readdirSync(dir)
        .reduce((files, file) =>
                fs.statSync(path.join(dir, file)).isDirectory() ?
                    files.concat(readDirRecurs(path.join(dir, file))) :
                    files.concat(path.join(dir, file)),
            []);

module.exports = {readDirRecurs};