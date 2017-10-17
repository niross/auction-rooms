const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  cache: true,
  context: __dirname,
  entry: {
    experience: './experience/src/index.jsx',
    'provider-auction': './provider-auction/src/index.jsx',
    gallery: './gallery/src/index.jsx',
    'provider-auction-widget': './auction-widget/provider/src/index.jsx',
    'guest-auction-widget': './auction-widget/guest/src/index.jsx',
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
    loaders: [{
      test: /\.jsx?$/,
      exclude: /node_modules/,
      loaders: [
        'babel?presets[]=stage-0'
      ]
    }, {
      test: /\.less$/,
      loader: 'style!css!less'
    }, {
      test: /\.json$/,
      loader: 'json'
    }, {
      test: /\.css$/,
      loader: 'style!css'
    }]
  },
  resolve: {
    extensions: ['', '.js', '.jsx'],
    alias: {
      ie: 'component-ie',
      'isomorphic-fetch': 'fetch-mock-forwarder'
    }
  },
  debug: false,
  plugins: [
    new webpack.optimize.CommonsChunkPlugin('vendors', 'vendors.bundle.js', Infinity),
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin(),
    new BundleTracker({ filename: './webpack-stats-prod.json' }),
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production')
      }
    }),
    new webpack.SourceMapDevToolPlugin(
      'bundle.js.map',
      '\n//# sourceMappingURL=http://127.0.0.1:3001/dist/js/[url]'
    ),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/)
  ]
};
