# Billtracker (with grunt)

## What you need

(only tested on mac & ubuntu so far)

### Mac (better get that [brew](http://brew.sh/) going)
```
brew install node
brew install python
```

### Ubuntu
* If you don't have node installed, do that https://nodejs.org/en/download/
* Update npm https://docs.npmjs.com/getting-started/installing-node
* If pip isn't installed, go to https://pip.pypa.io/en/stable/installing/ and follow the instructions there to install pip

Install the remaining dependencies:
```
npm install -g grunt-cli
pip install virtualenv
```

## Installation

1. `git clone https://github.com/bill-tracker/billtracker_grunt.git`

2. `cd billtracker_grunt`

3. `virtualenv venv`

4. `source venv/bin/activate`

6. `grunt build`

8. `grunt devserver`

9. `grunt watch` (in another terminal, to watch for stylesheet changes)

Go to localhost:8000 to test



### We're using sass for our css
We are using sass for our css.  To compile the scss to css manually use `grunt sassy`.  You can also run `grunt watch` and anytime you save any file in src it will compile your scss to css and also copy src to dev.

### css & js are minified in dist
`styles/src` contains our sass files. These files are compiled into css and placed in `styles/dev` while running `grunt watch` or after a `grunt sassy` command. The `grunt cssmin` command takes everything in `styles/dev` and minifies that file. Javascript files are stored in `scripts/src`.  `grunt compressjs` takes all script files and outputs them to one minified file in `scripts/dist`.

### Grunt Commands
Here are all our grunt commands:


`clean:styles`, `clean:scripts`, or `clean:all` - cleanup build artifacts (or `git clean -f`)

`grunt migrate` - runs python manage.py migrate

`grunt devserver` - runs python manage.py runserver, go to localhost:8000 to see the build in your brower

`grunt sassy` - compiles the scss to css

`grunt cssmin` - combines and minifies css

`grunt compressjs` - combines and minifies javascript

`grunt watch` - watches `styles/src` for any time you save a file.  When you do, it runs `grunt sassy`

