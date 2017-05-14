#!/usr/bin/env python

""" Resource Difference Checker
    Version 0.0.1 
"""

import hashlib
import logging
import sys
from datetime import date

from classes.resource import Resource
from classes.dbmanager import ResourceStorage
from classes.reporter import HtmlReport
import helpers

def get_reports_path(path=None):
    today = date.today()
    return "{0}/{1}/{2}/".format(path, today.month, today.day) if path else "reports/{0}/{1}/".format(today.month, today.day)

def check_differences(resources, report):
    report.add_urls(resources)
    changed_resources = []

    for resource in resources:
        actual_content = helpers.fetch_resource(resource.url)
        if actual_content:
            if (hashlib.sha256(actual_content).hexdigest() != resource.content.hash):
                report.add(resource, actual_content)
                
                resource.update(actual_content)
                changed_resources.append(resource)

    report.save()
    return changed_resources

if __name__ == "__main__":
    if len(sys.argv) != 1 and len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: %s [db_path] [reports_path]" % sys.argv[0])
        sys.exit()

    logging.basicConfig(filename='process.log',level=logging.DEBUG)

    db = sys.argv[1] if len(sys.argv) >= 2 else "data/resources.db"
    reports_path = get_reports_path(sys.argv[2]) if len(sys.argv) == 3 else get_reports_path()

    storage = ResourceStorage(db)
    if not storage.load():
        sys.exit()

    report = HtmlReport(reports_path, "diff.html")

    changed_resources = check_differences(storage.getall(), report)

    if changed_resources:
        storage.add_multiple(changed_resources)