#!/usr/bin/env python

""" Resource Difference Checker - Initialize
    Version 0.0.1
"""

import logging
import sys
import os

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
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: %s <url_list> [output_db_path]" % sys.argv[0])
        sys.exit()
    if sys.argv.count == 3:
        output = sys.argv[2]
        urls = sys.argv[1]
    else:
        output = "data/resources.db"
        urls = sys.argv[1]

    logging.basicConfig(filename='process.log',level=logging.DEBUG)
        
    with open(urls) as f:
       content = f.readlines()

    if os.path.exists(output):
        if helpers.get_user_input("The file '%s' already exists. Overwrite?" % output) and helpers.get_user_input("The original file will be gone. Are you sure?"):
            os.remove(output)

    storage = ResourceStorage(output)
    if not storage.create():
        sys.exit()

    counter = helpers.Counter()
    for url in filter_input(set(content)):
        process_resource(url, storage, counter)

    print("Added %s resources to DB." % counter.count)
    print("Done. Bye.")