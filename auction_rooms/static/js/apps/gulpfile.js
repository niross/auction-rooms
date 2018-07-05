const gulp = require('gulp');
const gutil = require('gulp-util');
const shell = require('gulp-shell');
const webpack = require('webpack');
const rimraf = require('gulp-rimraf');

const buildCfg = require('./webpack.config');

// ----------------------------------------------------------------------------
// Constants
// ----------------------------------------------------------------------------
const FRONTEND_FILES = [
  '*/src/**/*.jsx',
  '*/src/**/*.js'
];


// ----------------------------------------------------------------------------
// Cleaning
// ----------------------------------------------------------------------------
gulp.task('clean', () =>
  gulp
    .src([
      'dist/css',
      'dist/js'
    ], { read: false })
    .pipe(rimraf())
);

// Testing
// ----------------------------------------------------------------------------
gulp.task('test', shell.task(['npm run test']));

// ----------------------------------------------------------------------------
// Production
// ----------------------------------------------------------------------------
gulp.task('build:prod', (done) => {
  webpack(buildCfg).run((err, stats) => {
    if (err) { throw new gutil.PluginError('webpack', err); }

    gutil.log('[webpack]', stats.toString({
      hash: true,
      colors: true,
      cached: false
    }));

    done();
  });
});

gulp.task('build:prod-full', ['clean'], () =>
  gulp.run('build:prod')
);

gulp.task('watch:prod', () => {
  gulp.watch([
    'client/**/*.{js,jsx}'
  ], ['build:prod']);
});

// Hot reload webpack server
gulp.task('hotload', shell.task(['node ./server']));


// ----------------------------------------------------------------------------
// Aggregations
// ----------------------------------------------------------------------------
gulp.task('build-dev', ['build:dev']);
gulp.task('build', ['build:prod-full']);

