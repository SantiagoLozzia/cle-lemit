const path = require('path');

module.exports = {
  outputDir: path.resolve(__dirname, '../dist'),
  assetsDir: 'static',
  publicPath: '/',
  devServer: {
    host: 'cle-lemit.local',
    port: 8080,
    proxy: {
      '^/api': {
        target: 'http://192.168.100.10:8000',
        ws: true,
        changeOrigin: true,
      },
      '^/ws': {
        target: 'http://192.168.100.10:8000',
        ws: true,
        changeOrigin: true,
      },
    },
    allowedHosts: ['cle-lemit.local'],
  },
  transpileDependencies: ['vue'],
};
