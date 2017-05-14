#!/usr/bin/env python

""" Resource Difference Checker - Resource
    Version 0.0.1 
"""

from datetime import datetime
import hashlib
import zlib

class Content:
	def __init__(self, content):
		self.raw = content
		self.compressed = zlib.compress(content)
		self.hash = hashlib.sha256(content).hexdigest()

class Resource:
	def __init__(self, url, content, date=datetime.now()):
		self.url = url
		self.content = Content(content)
		self.date = date

	def update(self, content):
		self.content = Content(content)
		self.date = datetime.now()

	def toString():
		return ""


