# billtracker_grunt

Ok, I just pulled this down and got it working so we should be good.

This whole folder is a mac virtual environment (http://docs.python-guide.org/en/latest/dev/virtualenvs/).

## Steps to get this working

(only tested on mac & ubuntu so far)

* If you don't have node installed, do that https://nodejs.org/en/download/

* Update npm https://docs.npmjs.com/getting-started/installing-node

* Install Grunt if it's not already by typing `npm install -g grunt-cli`

1. `git clone https://github.com/bill-tracker/billtracker_grunt.git`

2. `cd billtracker_grunt`

3. `source bin/activate`

4. `npm install`

5. `pip install -r requirements.txt`

6. `grunt devserver`

Then go to localhost:8000

-- Mark 6/3, 7pm

### Why are there src, dev & dist folders?
So for this project we are working in the src folder and then outputting to both the dev and dist folders.  Dev is for viewing while working in src and dist is the production version.  Right now the only difference between dev and dist is that the css & js are each compressed to one minified file on dist.

### We're using sass for our css
We are using sass for our css.  To compile the scss to css manually use `grunt sassy`.  You can also run `grunt watchsass` and anytime you save any file in src it will compile your scss to css and also copy src to dev.

### css & js are minified in dist
The way we're dealing with css in src is that there's a css, scss and cssmin folder.  We're making all changes to the scss files.  Then we compile the scss to css with `sassy` or `watchsass`.  Then the `grunt mincss` command takes everything in the css folder and combines it to one file and minifies that file.  Similarly with javascript, src has a js and jsmin folder.  `grunt compressjs` takes all the js in the js folder and outputs it to one minified file in jsmin.  The grunt devcopy and dist copy are tweaked so they don't copy the scss folder over or the cssmin or jsmin folder.  distcopy only copies the minified css & js files, not all the others.

### Grunt Commands
Here are all our grunt commands:

`grunt devclean` - delete the dev folder

`grunt distclean` - delete the dist folder

`grunt devcopy` - copy src to dev

`grunt distcopy` - copy src to dist

`grunt devmigrate` - runs python manage.py makemigrations & python manage.py
 migrate on dev
 
`grunt distmigrate` - runs python manage.py makemigrations & python manage.py
 migrate on dist

`grunt devserver` - runs python manage.py runserver in dev, go to
 localhost:8000 to see the dev build in your brower

`grunt distserver` - runs python manage.py runserver in dev, go to
 localhost:8000 to see the dist build in your brower

`grunt sassy` - compiles the scss to css

`grunt compressjs` - combines and minifies the js to jsmin/scripts.min.js

`grunt mincss` - combines and minifies the css to cssmin/scripts.min.js

`grunt watchsass` - watches src for any time you save a file.  When you do,
 it runs `grunt sassy` and `grunt devcopy`

`grunt` - just running `grunt` by itself does all the hard work and gets both
 dev and dist ready to view.  It compiles, minifies and copies both dev and dist
