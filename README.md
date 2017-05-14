# Resource Difference Checker

The idea is to track updates made to resource avaialable on the web. Expected are JS files or whole HTML pages as jsbeautifier (https://github.com/beautify-web/js-beautify) is run on the compared contents. Resources are stored in a sqlite3 DB. A HTML report is generated for all processed URLs.

# Usage

The are two important python scripts ```initialize.py``` and ```diffcheck.py```. The first takes a list of domains (see example ```resources.txt```) and creates a initial DB. The latter mentioned is ment to be scheduled to run once a day and works with a DB created by ```initialize.py```.

```
usage: initialize.py [-h] [-l LOGFILE] urls output_db
usage: diffcheck.py [-h] [-l LOGFILE] db report_dir
```

```
$ cat resources.txt
# Comments are ignored
http://example.com/scripts/x.js
https://example.com/page.html
```

# Setup

```
$ python3.6 -m pip install jsbeautifier
$ git clone https://github.com/bayotop/resdiffcheck
$ cd resdiffcheck/resdiffcheck
$ python3.6 initialize.py resources.txt data/resources.db
$ crontab -e 

0 23 * * * python3.6 ~/resdiffcheck/resdiffcheck/diffcheck.py ~/resdiffcheck/resdiffcheck/data/resources.db ~/public_html/resdiffcheck/reports
```


