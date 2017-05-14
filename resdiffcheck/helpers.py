#!/usr/bin/env python

""" Resource Difference Checker - Helper methods
    Version 0.0.1 
"""

import requests
import logging

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count

def fetch_resource(url): 
    try:
        return requests.get(url).content
    except KeyboardInterrupt:
            logging.info("Fetch interrupted by user...")
    except Exception as e:
            logging.warning("Failed to fetch %s: %s" % (url, str(e)))

def get_user_input(message):
    return input("%s (y/N): " % message).lower() == 'y'