#!/usr/bin/env python

import argparse
import logging
import os
import sys
import textwrap

from classes.resource import Resource
from classes.dbmanager import ResourceStorage
import helpers

def filter_input(input):
    for l in input:
        line = l.strip()
        if line and not line.startswith("#"):
            yield line

def process_resource(url, storage, counter=None):
    content = helpers.fetch_resource(url)

    if content:
        r = Resource(url, content)            
        if storage.add(r) and counter:
            counter.increment()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="initialize.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
            Resource Difference Checker - Initialize
            
            See https://github.com/bayotop/resdiffcheck for more information.
            """))

    parser.add_argument("urls", help="file containing a list of URLs to resources")
    parser.add_argument("output_db", help="name of output DB with processed urls")
    parser.add_argument("-l", "--logfile", default="process.log",  help="default ./process.log")
    args = parser.parse_args()

    logging.basicConfig(filename=args.logfile,level=logging.DEBUG)
        
    with open(args.urls) as f:
       content = f.readlines()

    if os.path.exists(args.output_db):
        if helpers.get_user_input("The file '%s' already exists. Overwrite?" % args.output_db) and helpers.get_user_input("The original file will be gone. Are you sure?"):
            os.remove(args.output_db)

    storage = ResourceStorage(args.output_db)
    if not storage.create():
        sys.exit()

    counter = helpers.Counter()
    for url in filter_input(set(content)):
        process_resource(url, storage, counter)

    print("Added %s resources to DB." % counter.count)
    print("Done. Bye.")