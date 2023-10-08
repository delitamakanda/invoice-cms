const { defineConfig } = require('@vue/cli-service')
const BundleTacker = require('webpack-bundle-tracker')
const NodePolyfillPlugin = require('node-polyfill-webpack-plugin')

module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/static/': 'http://0.0.0.0:8080',
  outputDir: './dist/',

  configureWebpack: {
    plugins: [
      new NodePolyfillPlugin()
    ],
    optimization: {
      splitChunks: {
        chunks: 'all'
      }
    }
  },

  chainWebpack: config => {
    config.optimization.splitChunks(false)

    config.plugin('BundleTacker').use(BundleTacker, [{filename: 'webpack-stats.json'}])

    config.resolve.alias.set('__STATIC__', 'static')

    config.devServer
    .host('0.0.0.0')
    .port(8080)
    .hot(true)
    .https(false)
    .headers({"Access-Control-Allow-Origin": ["\*"]})
  }
})
