# Resource Difference Checker

The idea is to track updates made to resource avaialable on the web. Preferred are JS files or whole HTML pages.
The are two important python scripts ```initialize.py``` and ```diffcheck.py```. The latter mentioned is ment to be scheduled to run once a day.

Before a difference report is created jsbeautifier (https://github.com/beautify-web/js-beautify) is run on the compared contents.  

# Setup

```
$ python3.6 -m pip install jsbeautifier
$ git clone https://github.com/bayotop/resdiffcheck
$ cd resdiffcheck/resdiffcheck
$ echo "http://example.com/js/script.js" >> resources.txt
$ python3.6 initialize.py resources.txt data/resources.db
$ python3.6 diffcheck.py data/resources.db ~/public_html/resdiffcheck/reports

```


