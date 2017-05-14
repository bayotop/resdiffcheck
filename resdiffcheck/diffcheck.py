#!/usr/bin/env python

import argparse
from datetime import date
import hashlib
import logging
import sys
import textwrap

from classes.resource import Resource
from classes.dbmanager import ResourceStorage
from classes.reporter import HtmlReport
import helpers

def get_reports_path(path):
    today = date.today()
    return "{0}/{1}/{2}/".format(path, today.month, today.day)

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
    parser = argparse.ArgumentParser(
        prog="diffcheck.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
            Resource Difference Checker
            
            See https://github.com/bayotop/resdiffcheck for more information.
            """))

    parser.add_argument("db", help="database with resources to check")
    parser.add_argument("report_dir", help="target directory for reports (without trailing /)")
    parser.add_argument("-l", "--logfile", default="process.log",  help="default ./process.log")
    args = parser.parse_args()

    logging.basicConfig(filename=args.logfile,level=logging.DEBUG)


    storage = ResourceStorage(args.db)
    if not storage.load():
        sys.exit()

    report = HtmlReport(get_reports_path(args.report_dir), "diff.html")

    changed_resources = check_differences(storage.getall(), report)

    if changed_resources:
        storage.add_multiple(changed_resources)