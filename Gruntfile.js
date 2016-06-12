module.exports = function(grunt) {

  grunt.initConfig({
    env : {
      dev: { DJANGO_SETTINGS_MODULE : 'billtracker.settings' },
      prod: { DJANGO_SETTINGS_MODULE : 'billtracker.prodsettings' }
    },
    clean: {
      styles: {
        src: [
          'billtracker/bills/static/bills/styles/dist', 
          'billtracker/bills/static/bills/styles/dev'
        ]
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
        options: { style: 'expanded' },
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
      options: { shorthandCompacting: true },
      target: {
        files: {
          'billtracker/bills/static/bills/styles/dist/style.min.css':
            'billtracker/bills/static/bills/styles/dev/*'
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
          'billtracker/bills/static/bills/scripts/dist/scripts.min.js' :
            [ 'billtracker/bills/static/bills/scripts/dist/scripts.min.js' ]
        }
      }
    },
    exec: {
      restore: { cmd: 'npm install && pip install -r requirements.txt' }
    },
    'django-manage': {
      options: {
        app: 'billtracker',
        manage_path: './billtracker/'
      },
      serve: {
        options: {
          command: 'runserver',
          args: []
        }
      },
      migrate: {
        options: {
          command: 'migrate',
          args: []
        }
      },
      migration: {
        options: {
          command: 'makemigrations',
          args: []
        }
      },
      crawl: {
        options: {
          command: 'crawlLegiscan',
          verbose: true
        }
      }
      // test: {
      // }
    },
    'django-admin': {
      options: {
        app: 'billtracker',
        manage_path: './billtracker/'
      }
    },
    watch: {
      files: 'billtracker/bills/static/bills/styles/src/*',
      tasks: ['sassy']
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
  grunt.loadNpmTasks('grunt-contrib-django');

  grunt.registerTask('restore', ['exec:restore']);
  grunt.registerTask('clean:all', ['clean:styles', 'clean:scripts']);
  grunt.registerTask('sassy', ['sass:dev']);
  grunt.registerTask('compressjs', ['concat', 'uglify']);
  grunt.registerTask('migration', ['django-manage:migrate']);
  grunt.registerTask('migrate', ['django-manage:migration']);

  grunt.registerTask('build', ['restore', 'clean:all', 'copy:deps', 'sassy', 'cssmin', 'compressjs', 'migrate']);
  grunt.registerTask('devserver', ['env:dev', 'django-manage:serve']);
  grunt.registerTask('prodserver', ['env:prod', 'django-manage:serve']);
};
