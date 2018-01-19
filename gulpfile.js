const gulp = require('gulp')
const rollup = require('rollup')

// Gulp plugins
const sass = require('gulp-sass')
const cleancss = require('gulp-clean-css')
const csscomb = require('gulp-csscomb')
const autoprefixer = require('gulp-autoprefixer')

// Rollup plugins
const buble = require('rollup-plugin-buble')
const commonjs = require('rollup-plugin-commonjs')
const globals = require('rollup-plugin-node-globals')
const resolve = require('rollup-plugin-node-resolve')
const uglify = require('rollup-plugin-uglify')

const project_base = './src/nouvelles/static/'

const paths = {
  source: {
    scss: project_base + 'src/scss/*.scss',
    js: project_base + 'src/js/app.js',
  },
  dest: {
    css: project_base + 'css',
    js: project_base + 'js/teamlogger.js'
  },
}

/* Begin build tasks definition */

gulp.task('build:styles', () => {
  return gulp.src(paths.source.scss)
    .pipe(sass({ outputStyle: 'compact', precision: 10 })
      .on('error', sass.logError)
    )
    .pipe(autoprefixer())
    .pipe(csscomb())
    .pipe(cleancss())
    .pipe(gulp.dest(paths.dest.css))
})

gulp.task('build:js', () => {
  return rollup.rollup({
    input: paths.source.js,
    plugins: [
      buble(),
      resolve({ browser: true, jsnext: true, main: true }),
      commonjs(),
      globals(),
      uglify()
    ]
  }).then(bundle => {
    return bundle.write({
      file: paths.dest.js,
      format: 'iife',
      sourcemap: true,
    })
  })
})

/* End of build tasks definition */

/* Begin watch tasks definition */

gulp.task('watch:styles', () => {
  gulp.watch(project_base + 'src/scss/**/*.scss', ['build:styles'])
})

gulp.task('watch:js', () => {
  gulp.watch(project_base + 'src/js/**/*', ['build:js'])
})

/* End of watch tasks definition */

gulp.task('watch', ['watch:styles', 'watch:js'])
gulp.task('build', ['build:styles', 'build:js'])
gulp.task('default', ['build'])
