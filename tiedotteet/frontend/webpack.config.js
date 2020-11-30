const path = require('path')
const webpack = require('webpack')
const HtmlWebPackPlugin = require('html-webpack-plugin')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')

module.exports = (env) => {
  return {
    entry: './src/index.js',
    output: {
      path: path.resolve(__dirname, 'public/tiedotteet'),
      filename: 'tiedotteet-bundle.js',
      publicPath: '/static/tiedotteet/',
    },
    devtool: 'source-map',
    devServer: {
      contentBase: path.resolve(__dirname, 'public/tiedotteet'),
      port: '3000',
    },
    module: {
      rules: [
        {
          test: /\.scss$/i,
          use: [
            'style-loader',
            'css-loader',
            'resolve-url-loader',
            'sass-loader',
          ],
        },
        {
          test: /\.js$/i,
          exclude: /node_modules/,
          use: 'babel-loader',
        },
        {
          test: /\.(png|svg|jpg|gif)$/i,
          type: 'asset/resource',
        },
        {
          test: /\.(woff|woff2|eot|ttf|otf)$/i,
          type: 'asset/resource',
        },
      ],
    },
    resolve: {
      extensions: ['.js', '.jsx'],
    },
    plugins: [
      new CleanWebpackPlugin(),
      new webpack.HotModuleReplacementPlugin(),
      new HtmlWebPackPlugin({
        inject: env.development ? true : false,
        template: env.development ? './src/index_dev.html' : './src/index.html',
      }),
    ],
  }
}
