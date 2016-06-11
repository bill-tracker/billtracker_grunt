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
    clean: {
      styles: {
        src: ['billtracker/bills/static/bills/styles/dist', 'billtracker/bills/static/bills/styles/dev']
      },
      scripts: {
        src: ['billtracker/bills/static/bills/scripts/dist']
      }
    },
    copy: {
      deps: {
        files: [{
            expand: true,
            cwd: 'node_modules/bootstrap/dist/css/',
            src: ['bootstrap.css', 'bootstrap.css.map'],
            dest: 'billtracker/bills/static/bills/styles/dev'
        },{
            expand: true,
            cwd: 'node_modules/intro.js/',
            src: ['introjs.css'],
            dest: 'billtracker/bills/static/bills/styles/dev'
        },{
            expand: true,
            cwd: 'node_modules/bootstrap/dist/js/',
            src: ['bootstrap.js'],
            dest: 'billtracker/bills/static/bills/scripts/src'
        },{
            expand: true,
            cwd: 'node_modules/intro.js/',
            src: ['intro.js'],
            dest: 'billtracker/bills/static/bills/scripts/src'
        }],
      }
    },
    sass: {
      dev: {
        options: {
          style: 'expanded'
        },
        files: [{
          expand: true,
          cwd: 'billtracker/bills/static/bills/styles/src',
          src: ['*.scss'],
          dest: 'billtracker/bills/static/bills/styles/dev',
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
          'billtracker/bills/static/bills/styles/dist/style.min.css': 'billtracker/bills/static/bills/styles/dev/*'
        }
      }
    },
    concat: {
        js : {
            src : ['billtracker/bills/static/bills/scripts/src/*'],
            dest : 'billtracker/bills/static/bills/scripts/dist/scripts.min.js'
        }
    },
    uglify : {
        js: {
            files: {
                'billtracker/bills/static/bills/scripts/dist/scripts.min.js' : [ 'billtracker/bills/static/bills/scripts/dist/scripts.min.js' ]
            }
        }
    },
    exec: {
      // devmigrate: {
      //   cmd: function() {
      //     var commands = ''
      //     commands += 'cd dev/billtracker;'
      //     commands += 'python manage.py makemigrations;'
      //     commands += 'python manage.py migrate;'
      //     return commands
      //   }
      // },
      // devserver: {
      //   cmd: function() {
      //     var commands = ''
      //     commands += 'cd dev/billtracker;'
      //     commands += 'python manage.py runserver;'
      //     commands += 'echo http://127.0.0.1:8000/;'
      //     return commands
      //   }
      // },
    },
    watch: {
      files: 'billtracker/bills/static/bills/styles/src/*',
      tasks: ['build:css']
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

  // grunt.registerTask('devclean', ['clean:dev']);
  // grunt.registerTask('distclean', ['clean:dist']);
  // grunt.registerTask('devcopy', ['env:dev','copy:dev','preprocess:dev']);
  // grunt.registerTask('distcopy', ['env:dist','copy:distmain','copy:distcss','copy:distjs', 'copy:distreq', 'preprocess:dist']);
  // grunt.registerTask('devmigrate', ['exec:devmigrate']);
  // grunt.registerTask('distmigrate', ['exec:distmigrate']);
  // grunt.registerTask('devserver', ['exec:devserver']);
  // grunt.registerTask('distserver', ['exec:distserver']);
  // grunt.registerTask('sassy', ['sass:dev']);
  // grunt.registerTask('compressjs', ['concat:js','uglify:js']);
  // grunt.registerTask('mincss', ['cssmin']);
  // grunt.registerTask('watchsass', ['watch']);
  // grunt.registerTask('default', ['mincss','compressjs','devclean','distclean','devcopy','distcopy','devmigrate','distmigrate']);
  // grunt.registerTask('build', ['sassy', 'mincss', 'compressjs', 'distclean', 'distcopy']);

  grunt.registerTask('clean:all', ['clean:styles', 'clean:scripts']);
  grunt.registerTask('build:css', ['sass:dev', 'cssmin']);
  grunt.registerTask('build:js', ['concat', 'uglify']);
  grunt.registerTask('build', ['clean:all', 'copy:deps', 'build:css', 'build:js'])
  


  // TODO
  // * BUILD CSS - SASS PROCESS, MINIFY?
  // * BUILD JS - CONCAT, MINIFY
  // * SET ENVIRONMENT
  // * MIGRATE
  // * START SERVER
  // * WATCH FOR CHANGES
  // * CLEAN

};
