module.exports = function(grunt) {

  'use strict';

  require('time-grunt')(grunt);
  require('jit-grunt')(grunt, {
    // Static mappings below; needed because task name does not match package name
    bower: 'grunt-bower-task',
    usebanner: 'grunt-banner'
  });

  var path = require('path');

  // Allows a `--quiet` flag to be passed to Grunt from the command-line.
  // If the flag is present the value is true, otherwise it is false.
  // This flag can be used to, for example, suppress warning output
  // from linters.
  var env = {
    quiet: grunt.option('quiet') ? true : false
  };

  var config = {

    /**
     * Pull in the package.json file so we can read its metadata.
     */
    pkg: grunt.file.readJSON('bower.json'),

    /**
     * Set some src and dist location variables.
     */
    loc: {
      src: 'src',
      dist: '../static/',
      prod: '../cafi/core/templates/',
    },

    ngAnnotate: {
        app: {
            files: {
                '<%= loc.src %>/static/js/annotated/app-annotated.js': ['<%= loc.src %>/static/js/app.js'],
                '<%= loc.src %>/static/js/annotated/app-controller-annotated.js': ['<%= loc.src %>/static/js/app-controller.js'],
                '<%= loc.src %>/static/js/annotated/chartFilter-annotated.js': ['<%= loc.src %>/static/js/directives/chartFilter.js'],
                '<%= loc.src %>/static/js/annotated/dateInput-annotated.js': ['<%= loc.src %>/static/js/directives/dateInput.js'],
                '<%= loc.src %>/static/js/annotated/pillFilter-annotated.js': ['<%= loc.src %>/static/js/directives/pillFilter.js'],
                '<%= loc.src %>/static/js/annotated/client-service-annotated.js': ['<%= loc.src %>/static/js/client-service.js'],
                '<%= loc.src %>/static/js/annotated/export-service-annotated.js': ['<%= loc.src %>/static/js/export-service.js'],
                '<%= loc.src %>/static/js/annotated/project-service-annotated.js': ['<%= loc.src %>/static/js/project-service.js'],
            },
        }
    },

    /**
     * Concat: https://github.com/gruntjs/grunt-contrib-concat
     *
     * Concatenate cf-* Less files prior to compiling them.
     */
    concat: {
      js: {
        src: [
          '<%= loc.src %>/vendor/jquery/dist/jquery.js',
          '<%= loc.src %>/vendor/jquery.easing/js/jquery.easing.js',
          '<%= loc.src %>/vendor/cf-*/src/js/*.js',
          '<%= loc.src %>/vendor/d3/d3.min.js',
          '<%= loc.src %>/vendor/css-modal/modal.js',
          '<%= loc.src %>/vendor/angular/angular.min.js',
          '<%= loc.src %>/vendor/cf-expandables/src/js/cf-expandables.js',
          '<%= loc.src %>/vendor/angular-sanitize/angular-sanitize.min.js',
          '<%= loc.src %>/vendor/angular-resource/angular-resource.min.js',
          '<%= loc.src %>/vendor/angular-route/angular-route.min.js',
          '<%= loc.src %>/vendor/elasticsearch/elasticsearch.angular.min.js',
          '<%= loc.src %>/vendor/pikaday/pikaday.js',
          '<%= loc.src %>/vendor/moment/min/moment.min.js',
          '<%= loc.src %>/vendor/elastic.js/dist/elastic.min.js',
          '<%= loc.src %>/vendor/angular-bootstrap/ui-bootstrap-tpls.js',
          '<%= loc.src %>/vendor/nya-bootstrap-select/dist/js/nya-bs-select.min.js',
          '<%= loc.src %>/static/js/annotated/modal-controller-annotated.js',
          '<%= loc.src %>/static/js/annotated/chartFilter-annotated.js',
          '<%= loc.src %>/static/js/annotated/dateInput-annotated.js',
          '<%= loc.src %>/static/js/annotated/client-service-annotated.js',
          '<%= loc.src %>/static/js/annotated/export-service-annotated.js',
          '<%= loc.src %>/static/js/annotated/app-annotated.js',
          '<%= loc.src %>/static/js/annotated/project-service-annotated.js',
          '<%= loc.src %>/static/js/annotated/app-controller-annotated.js',
        ],
        dest: '<%= loc.dist %>/js/main.js'
      }
    },

    /**
     * Less: https://github.com/gruntjs/grunt-contrib-less
     *
     * Compile Less files to CSS.
     */
    less: {
      main: {
        options: {
          // The src/vendor paths are needed to find the CF components' files.
          // Feel free to add additional paths to the array passed to `concat`.
          paths: grunt.file.expand('src/vendor/*').concat([])
        },
        files: {
          '<%= loc.dist %>/css/main.css': ['<%= loc.src %>/static/css/main.less']
        }
      }
    },

    /**
     * Autoprefixer: https://github.com/nDmitry/grunt-autoprefixer
     *
     * Parse CSS and add vendor-prefixed CSS properties using the Can I Use database.
     */
    autoprefixer: {
      options: {
        // Options we might want to enable in the future.
        diff: false,
        map: false
      },
      main: {
        // Prefix `static/css/main.css` and overwrite.
        expand: true,
        src: ['<%= loc.dist %>/css/main.css']
      },
    },

    /**
     * Uglify: https://github.com/gruntjs/grunt-contrib-uglify
     *
     * Minify JS files.
     * Make sure to add any other JS libraries/files you'll be using.
     * You can exclude files with the ! pattern.
     */
    uglify: {
      options: {
        preserveComments: 'some',
        sourceMap: true,
        mangle: false
      },
      // headScripts: {
      //   src: 'vendor/html5shiv/html5shiv-printshiv.js',
      //   dest: 'static/js/html5shiv-printshiv.js'
      // },
      js: {
        src: ['<%= loc.dist %>/js/main.js'],
        dest: '<%= loc.dist %>/js/main.min.js'
      }
    },

    usebanner: {
      css: {
        options: {
          position: 'top',
          banner: '<%= banner %>',
          linebreak: true
        },
        files: {
          src: ['<%= loc.dist %>/css/*.min.css']
        }
      },
      js: {
        options: {
          position: 'top',
          banner: '<%= banner %>',
          linebreak: true
        },
        files: {
          src: ['<%= loc.dist %>/js/*.min.js']
        }
      }
    },

    /**
     * CSS Min: https://github.com/gruntjs/grunt-contrib-cssmin
     *
     * Compress CSS files.
     */
    cssmin: {
      main: {
        options: {
          processImport: false
        },
        files: {
          '<%= loc.dist %>/css/main.min.css': ['<%= loc.dist %>/css/main.css'],
        }
      },
      'ie-alternate': {
        options: {
          processImport: false
        },
        files: {
          '<%= loc.dist %>/css/main.ie.min.css': ['<%= loc.dist %>/css/main.ie.css'],
        }
      }
    },

    /**
     * Legacssy: https://github.com/robinpokorny/grunt-legacssy
     *
     * Fix your CSS for legacy browsers.
     */
    legacssy: {
      'ie-alternate': {
        options: {
          // Flatten all media queries with a min-width over 960 or lower.
          // All media queries over 960 will be excluded fromt he stylesheet.
          // EM calculation: 960 / 16 = 60
          legacyWidth: 60
        },
        files: {
          '<%= loc.dist %>/css/main.ie.css': '<%= loc.dist %>/css/main.css'
        }
      }
    },

    /**
     * Clean: https://github.com/gruntjs/grunt-contrib-clean
     *
     * Clean files and folders
     */
    // clean: ['../static/*'],

    /**
     * Copy: https://github.com/gruntjs/grunt-contrib-copy
     *
     * Copy files and folders.
     */
    copy: {
      main: {
        files: [
          {
            expand: true,
            cwd: '<%= loc.src %>',
            src: [
              // HTML files
              '*.html',
              'partial/**/*.html',
            ],
            dest: '<%= loc.dist %>/'
          },
          {
            expand: true,
            cwd: '<%= loc.src %>/static',
            src: [
              'images/**/*',
            ],
            dest: '<%= loc.dist %>'
          },
          {
            expand: true,
            flatten: true,
            cwd: '<%= loc.src %>',
            src: [
              // Fonts
              'vendor/cf-icons/src/fonts/*'
            ],
            dest: '<%= loc.dist %>/fonts'
          },
          {
            expand: true,
            cwd: '<%= loc.src %>',
            src: [
              // Vendor files
              'vendor/box-sizing-polyfill/boxsizing.htc',
            ],
            dest: '<%= loc.dist %>/'
          },
          {
            expand: true,
            cwd: '<%= loc.src %>',
            src: [
              // Vendor files
              '*.html',
            ],
            dest: '<%= loc.prod %>/'
          },          
        ]
      }
    },

    /**
     * Lint the JavaScript.
     */
    lintjs: {
      /**
       * Validate files with ESLint.
       * https://www.npmjs.com/package/grunt-contrib-eslint
       */
      eslint: {
        options: {
          quiet: env.quiet
        },
        src: [
          // 'Gruntfile.js', // Uncomment to lint the Gruntfile.
          '<%= loc.src %>/static/js/app.js'
        ]
      }
    },

    /**
     * Watch: https://github.com/gruntjs/grunt-contrib-watch
     *
     * Run predefined tasks whenever watched file patterns are added, changed or deleted.
     * Add files to monitor below.
     */
    watch: {
      default: {
        files: ['Gruntfile.js', '<%= loc.src %>/static/css/**/*.less', '<%= loc.src %>/static/js/*.js',
        '<%= loc.src %>/static/js/directives/*.js', '<%= loc.src %>/*.html', '<%= loc.src %>/partial/*.html'],
        tasks: ['default'],
      },
      options: {
          livereload: true,
      },
    }

  };

  /**
   * Initialize a configuration object for the current project.
   */
  grunt.initConfig(config);

  /**
   * Create custom task aliases and combinations.
   */
  grunt.loadNpmTasks('grunt-ng-annotate');
  grunt.registerTask('css', ['less', 'autoprefixer', 'legacssy', 'cssmin', 'usebanner:css']);
  grunt.registerTask('js', ['ngAnnotate:app', 'concat:js', 'usebanner:js']);
  grunt.registerTask('test', ['lintjs']);
  grunt.registerMultiTask('lintjs', 'Lint the JavaScript', function(){
    grunt.config.set(this.target, this.data);
    grunt.task.run(this.target);
  });
  grunt.registerTask('build', ['test', 'css', 'js', 'copy']);
  grunt.registerTask('default', ['build']);
};
