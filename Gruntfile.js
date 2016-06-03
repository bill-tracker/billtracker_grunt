module.exports = function(grunt) {

  grunt.initConfig({
    env : {
      dev: {
          NODE_ENV : 'DEVELOPMENT'
      },
      dist : {
          NODE_ENV : 'PRODUCTION'
      }
    },
    preprocess : {
      dev : {
        src : 'src/billtracker/bills/templates/bills/index.html',
        dest : 'dev/billtracker/bills/templates/bills/index.html'
      },
      dist : {
        src : 'src/billtracker/bills/templates/bills/index.html',
        dest : 'dist/billtracker/bills/templates/bills/index.html'
      }
    },
    copy: {
      dev: {
        files: [{
            expand: true,
            cwd: 'src/',
            src: ['*','**', '!**/scss/**', '!**/cssmin/**', '!**/jsmin/**'],
            dest: 'dev/'
        }],
      },
      distmain: {
        files: [{
            expand: true,
            cwd: 'src/',
            src: ['*','**', '!**/css/*', '!**/scss/**', '!**/cssmin/**', '!**/js/*', '!**/jsmin/**'],
            dest: 'dist/'
        }],
      },
      distcss: {
        files: [{
            expand: true,
            cwd: 'src/billtracker/bills/static/bills/cssmin/',
            src: ['style.min.css'],
            dest: 'dist/billtracker/bills/static/bills/css/'
        }],
      },
      distjs: {
        files: [{
            expand: true,
            cwd: 'src/billtracker/bills/static/bills/jsmin/',
            src: ['scripts.min.js'],
            dest: 'dist/billtracker/bills/static/bills/js/'
        }],
      },
    },
    clean: {
      dev: {
        src: ['dev/billtracker']
      },
      dist: {
        src: ['dist/billtracker/']
      }
    },
    exec: {
      devmigrate: {
        cmd: function() {
          var commands = ''
          commands += 'cd dev/billtracker;'
          commands += 'python manage.py makemigrations;'
          commands += 'python manage.py migrate;'
          return commands
        }
      },
      distmigrate: {
        cmd: function() {
          var commands = ''
          commands += 'cd dist/billtracker;'
          commands += 'python manage.py makemigrations;'
          commands += 'python manage.py migrate;'
          return commands
        }
      },
      devserver: {
        cmd: function() {
          var commands = ''
          commands += 'cd dev/billtracker;'
          commands += 'python manage.py runserver;'
          return commands
        }
      },
      distserver: {
        cmd: function() {
          var commands = ''
          commands += 'cd dist/billtracker;'
          commands += 'python manage.py runserver;'
          return commands
        }
      },
    },
    sass: {
      dev: {
        options: {
          style: 'expanded'
        },
        files: [{
          expand: true,
          cwd: 'src/billtracker/bills/static/bills/scss',
          src: ['*.scss'],
          dest: 'src/billtracker/bills/static/bills/css',
          ext: '.css'
        }]
      }
    },
    cssmin: {
      options: {
        shorthandCompacting: true
      },
      target: {
        files: {
          'src/billtracker/bills/static/bills/cssmin/style.min.css': 'src/billtracker/bills/static/bills/css/*'
        }
      }
    },
    concat: {
        js : {
            src : [
                'src/billtracker/bills/static/bills/js/*'
            ],
            dest : 'src/billtracker/bills/static/bills/jsmin/scripts.min.js'
        }
    },
    uglify : {
        js: {
            files: {
                'src/billtracker/bills/static/bills/jsmin/scripts.min.js' : [ 'src/billtracker/bills/static/bills/jsmin/scripts.min.js' ]
            }
        }
    },
    watch: {
      // files: 'src/billtracker/bills/static/bills/scss/**',
      files: 'src/billtracker/**',
      tasks: ['sass:dev','devcopy']
    }
  });

  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-env');
  grunt.loadNpmTasks('grunt-preprocess');
  grunt.loadNpmTasks('grunt-exec');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');

  grunt.registerTask('devclean', ['clean:dev']);
  grunt.registerTask('distclean', ['clean:dist']);
  grunt.registerTask('devcopy', ['env:dev','copy:dev','preprocess:dev']);
  grunt.registerTask('distcopy', ['env:dist','copy:distmain','copy:distcss','copy:distjs','preprocess:dist']);
  grunt.registerTask('devmigrate', ['exec:devmigrate']);
  grunt.registerTask('distmigrate', ['exec:distmigrate']);
  grunt.registerTask('devserver', ['exec:devserver']);
  grunt.registerTask('distserver', ['exec:distserver']);
  grunt.registerTask('sassy', ['sass:dev']);
  grunt.registerTask('compressjs', ['concat:js','uglify:js']);
  grunt.registerTask('mincss', ['cssmin']);
  grunt.registerTask('watchsass', ['watch']);
  grunt.registerTask('default', ['mincss','compressjs','devclean','distclean','devcopy','distcopy','devmigrate','distmigrate']);

};
