const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  cache: true,
  context: __dirname,
  mode: 'production',
  entry: {
    experience: './experience/src/index.jsx',
    'provider-auction': './provider-auction/src/index.jsx',
    gallery: './gallery/src/index.jsx',
    'provider-auction-widget': './auction-widget/provider/src/index.jsx',
    'guest-auction-widget': './auction-widget/guest/src/index.jsx',
    quickbid: './quickbid/src/index.jsx',
    vendors: [
      'react', 'react-dom', 'react-materialize', 'redux', 'redux-thunk',
      'react-redux', 'immutable', 'whatwg-fetch', 'isomorphic-fetch',
      'js-cookie', 'babel-polyfill'
    ]
  },
  output: {
    path: path.join(__dirname, 'dist/js'),
    filename: '[name].bundle.js'
  },
  module: {
    rules: [{
      test: /\.jsx?$/,
      exclude: /node_modules/,
      loaders: [
        'babel-loader?presets[]=stage-0'
      ]
    }, {
      test: /\.less$/,
      loader: 'style-loader!css!less'
    }, {
      test: /\.json$/,
      loader: 'json-loader'
    }, {
      test: /\.css$/,
      loader: 'style-loader!css-loader'
    }, {
      test: /.(png|jpg)$/,
      loader: 'file-loader',
      options: {
        publicPath: '/static/js/apps/dist/'
      }
    }]
  },
  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      ie: 'component-ie',
      'isomorphic-fetch': 'fetch-mock-forwarder'
    }
  },
  debug: false,
  optimization: {
    splitChunks: 'all'
  },
  optimization: {
    splitChunks: {
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendor',
          chunks: 'all'
        }
      }
    }
  },
  plugins: [
    // ensure that we get a production build of any dependencies
    // this is primarily for React, where this removes 179KB from the bundle
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': '"production"'
    }),
    new BundleTracker({ filename: './webpack-stats-prod.json' }),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/)
  ]
};
