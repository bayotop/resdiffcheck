#!/usr/bin/env python

""" Resource Difference Checker - Report 
    Version 0.0.1 
"""

from datetime import date
import difflib
from enum import Enum
from html import escape
import jsbeautifier
import os
import unicodedata

from helpers import Counter

DEFAULT_TEMPLATE = os.path.dirname(os.path.abspath(__file__)) + "/../html/report_layout.html"
MACRO_PATTERN = "#diffcheck#."

NO_ITEMS_TEMPLATE = """<li>No changes.</li>"""
MENU_ITEM_TEMPLATE = """<li><a href="{0}id.html">{0}url</a></li>""".format(MACRO_PATTERN)
LIST_ITEM_TEMPLATE = """<li><a href="{0}url">{0}url</a>&nbsp;<small>Last change: {0}last</span></small>""".format(MACRO_PATTERN)

def getMacroName(name):
    return "{0}{1}".format(MACRO_PATTERN, name)

class HtmlReport():
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.fullname = path + name
       
        self.__create()

    def __create(self):
        os.makedirs(os.path.dirname(self.fullname), exist_ok=True)

        with open(DEFAULT_TEMPLATE, 'r') as t:
            template = t.read()

        self.report = template
        self.counter = Counter()
        
        self.__eval("date", date.today().strftime("%B %d, %Y"))

    def __eval(self, pattern, replacement):
        self.report = self.report.replace(getMacroName(pattern), replacement)

    def add(self, resource, actual_content):
        id = str(self.counter.increment())

        item = MENU_ITEM_TEMPLATE.replace(getMacroName("id"), id).replace(getMacroName("url"), resource.url)
        self.__eval("menu_item", getMacroName("menu_item") + item)

        report = difflib.HtmlDiff().make_file(
            jsbeautifier.beautify(resource.content.raw.decode("utf-8", "ignore")).splitlines(), 
            jsbeautifier.beautify(actual_content.decode("utf-8", "ignore")).splitlines())
        
        with open(self.path + id + ".html", 'wb') as r:
           r.write(report.encode())

    def add_urls(self, resources):
        list = []   
        for r in resources:
            list.append(LIST_ITEM_TEMPLATE.replace(getMacroName("url"), r.url).replace(getMacroName("last"), r.date.split(" ")[0]))

        self.__eval("list", "\n".join(list))

    def save(self):
        self.__eval("menu_item", "" if self.counter.count else NO_ITEMS_TEMPLATE)

        with open(self.fullname, 'w') as r:
           r.write(self.report)



        


