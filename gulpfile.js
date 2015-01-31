var gulp = require('gulp');

var uglify = require('gulp-uglify');
var sass = require('gulp-ruby-sass');

var paths = {
  jspath: ['web/static/js/**/*.js', '!web/static/js/common/libs/**/*.js'],
  css: ['app/static/assets/style.scss']
};


gulp.task('scss', function() {
  return sass(paths.css, { style: 'compressed', sourcemap: false})
    // .pipe(autoprefixer('last 2 version', 'safari 5', 'ie 8', 'ie 9', 'opera 12.1', 'ios 6', 'android 4'))
    .pipe(gulp.dest('app/static/css'))
});

gulp.task('watch', function() {
  // gulp.watch(paths.scripts, ['scripts']);
  gulp.watch(paths.css, ['scss']);
});

gulp.task('default', ['scss', 'watch']);
