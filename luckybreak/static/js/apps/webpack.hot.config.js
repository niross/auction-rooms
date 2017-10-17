const webpack = require('webpack');
const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');

const PUBLIC_PATH = 'http://localhost:3000';

module.exports = {
  devtool: 'eval',
  cache: true,
  context: __dirname,
  entry: {
    experience: [
      `webpack-dev-server/client?${PUBLIC_PATH}`,
      'webpack/hot/only-dev-server',
      './experience/src/index.jsx'
    ],
    'provider-auction': [
      `webpack-dev-server/client?${PUBLIC_PATH}`,
      'webpack/hot/only-dev-server',
      './provider-auction/src/index.jsx'
    ],
    gallery: [
      `webpack-dev-server/client?${PUBLIC_PATH}`,
      'webpack/hot/only-dev-server',
      './gallery/src/index.jsx'
    ],
    'provider-auction-widget': [
      `webpack-dev-server/client?${PUBLIC_PATH}`,
      'webpack/hot/only-dev-server',
      './auction-widget/provider/src/index.jsx'
    ],
    'guest-auction-widget': [
      `webpack-dev-server/client?${PUBLIC_PATH}`,
      'webpack/hot/only-dev-server',
      './auction-widget/guest/src/index.jsx'
    ],
    vendors: ['react', 'react-materialize']
  },
  output: {
    path: path.join(__dirname, '/dist/js'),
    filename: '[name].bundle.js',
    publicPath: `${PUBLIC_PATH}/static/js/apps/dist/js/`
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),
    new BundleTracker({ filename: './webpack-stats-dev.json' }),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/)
  ],
  resolve: {
    modulesDirectories: ['node_modules', 'bower_components'],
    extensions: ['', '.js', '.jsx'],
    alias: {
      ie: 'component-ie'
    }
  },
  module: {
    loaders: [{
      test: /\.jsx?$/,
      exclude: /node_modules/,
      loaders: ['react-hot', 'babel?presets[]=stage-0']
    }, {
      test: /\.css/,
      loader: 'style-loader!css-loader'
    }, {
      test: /\.less$/,
      loader: 'style!css!less'
    }, {
      test: /\.json$/,
      loader: 'json'
    }, {
      test: /\.jpe?g$|\.gif$|\.png$|\.ico$/,
      loader: `${require.resolve('file-loader')}?name=[name].[ext]`
    }, {
      test: /\.eot|\.ttf|\.svg|\.woff2?/,
      loader: `${require.resolve('file-loader')}?name=[name].[ext]`
    }]
  }
};

