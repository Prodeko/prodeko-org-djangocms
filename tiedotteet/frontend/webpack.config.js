const path = require('path')
const webpack = require('webpack')
const HtmlWebPackPlugin = require('html-webpack-plugin')

module.exports = env => {
  return {
    mode: env.production ? 'production' : 'development',
    entry: './src/index.js',
    output: {
      path: path.resolve(__dirname, 'public/tiedotteet'),
      filename: 'tiedotteet-bundle.js',
      publicPath: '/static/tiedotteet/'
    },
    devtool: 'source-map',
    devServer: {
      contentBase: path.resolve(__dirname, 'public/tiedotteet'),
      port: '3000'
    },
    module: {
      rules: [
        {
          test: /\.scss$/,
          use: ['style-loader', 'css-loader', 'sass-loader']
        },
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: ['babel-loader']
        },
        {
          test: /\.(png|svg|jpg|gif)$/,
          use: 'file-loader'
        },
        {
          test: /\.(woff|woff2|eot|ttf|otf)$/,
          use: ['file-loader']
        }
      ]
    },
    resolve: {
      extensions: ['.js', '.jsx']
    },
    plugins: [
      new webpack.HotModuleReplacementPlugin(),
      new HtmlWebPackPlugin({
        inject: env.development ? true : false,
        template: env.development ? './src/index_dev.html' : './src/index.html'
      })
    ]
  }
}
