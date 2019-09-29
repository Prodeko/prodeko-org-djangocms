const path = require('path');
const webpack = require('webpack');
const HtmlWebPackPlugin = require('html-webpack-plugin');
const publicPathProd = 'https://static.prodeko.org/';

module.exports = env => {
  return {
    mode: 'development',
    entry: './src/index.js',
    output: {
      path: path.resolve(__dirname, 'public/tiedotteet'),
      filename: 'tiedotteet-bundle.js',
      publicPath: env.production ? publicPathProd : '/tiedotteet/'
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
          test: /\.js(x)?$/,
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
        inject: false,
        template: './src/index.html'
      })
    ]
  };
};
