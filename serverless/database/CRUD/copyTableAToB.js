const getAll = require('./getAll');
const create = require('./create');

/**
 * Copy the items from TableA to TableB, both TableA and TableB needs to be defined
 * @param {string} tableNameA
 * @param {string} tableNameB
 * */
const copyTableAToB = (tableNameA, tableNameB) => {
  return getAll(tableNameA)
      .then(items => {
        let promises = items.map(item => {
          return create(tableNameB, item);
        });
        
        return Promise.all(promises)
      })
};

module.exports = copyTableAToB;