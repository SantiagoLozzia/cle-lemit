const path = require('path');

module.exports = {
  outputDir: path.resolve(__dirname, '../backend/cle_backend/static/vue'),
  indexPath: path.resolve(__dirname, '../backend/cle_backend/templates/index.html'),
  transpileDependencies: [
    'vue'
  ],
};
