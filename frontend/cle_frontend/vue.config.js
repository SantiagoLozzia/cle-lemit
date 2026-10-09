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
        target: 'http://localhost:8000',
        ws: true,
        changeOrigin: true,
      },
      '^/ws/mi_canal/': {
        target: 'http://localhost:8000',
        ws: true,
        changeOrigin: true,
      },
    },
    allowedHosts: ['cle-lemit.local'],
  },
  transpileDependencies: ['vue'],
};
