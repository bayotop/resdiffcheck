#!/usr/bin/env python

""" Resource Difference Checker - DB Manager
    Version 0.0.1 
"""

import logging
import helpers
import os
import sqlite3
import zlib

from classes.resource import Resource

TABLE_NAME = "resources"
URL_COLUMN = "url"
CONTENT_COLUMN = "content"
DATE_COLUMN = "date"

class ResourceStorage:
    def __init__(self, path):
        self.path = path
        self.connection = None

        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def __connect(self):
        if not self.connection:
            try:
                self.connection = sqlite3.connect(self.path)
            except Exception as e:
                logging.critical("Couldn't connect to %s: %s" % (self.path, str(e)))
                return None
        
        return self.connection.cursor();

    def __commit(self):
        if self.connection:
            try:
                self.connection.commit()
                self.connection.close()
                return True
            except Exception as e:
                logging.critical("Couldn't safely commit to %s: %s" % (self.path, str(e)))
            finally:
                self.connection = None

        return False

    def create(self):
        c = self.__connect()

        if not c:
            return False
        
        c.execute("CREATE TABLE %s(%s text primary key, %s text, %s timestamp)" % (TABLE_NAME, URL_COLUMN, CONTENT_COLUMN, DATE_COLUMN))
        logging.info("Creating DB table '%s'" % (TABLE_NAME))
        return self.__commit()

    def load(self):
        if os.path.exists(self.path):
            # Just to make sure we have access
            self.__connect()
            return self.__commit()

        logging.critical("Couldn't connect to %s: %s" % (self.path, "The file doesn't exist."))
        return False

    def getall(self):
       result = []
       
       c = self.__connect()
       if c:
            data = c.execute("SELECT %s, %s, %s FROM %s" % (URL_COLUMN, CONTENT_COLUMN, DATE_COLUMN, TABLE_NAME))
            for row in data:
                result.append(Resource(row[0], zlib.decompress(row[1]), row[2]))
            self.__commit();

       return result

    def add(self, resource):
        c = self.__connect()
        if c:
            c.execute("INSERT INTO %s VALUES (?, ?, ?)" % TABLE_NAME, (resource.url, sqlite3.Binary(resource.content.compressed), resource.date))
            logging.info("Adding '%s' on '%s'" % (resource.url, resource.date))
        return self.__commit()

    def add_multiple(self, resources):
        c = self.__connect()
        if c:
           for r in resources:
                c.execute("UPDATE %s SET %s = ?, %s = ? WHERE %s = ?" % (TABLE_NAME, CONTENT_COLUMN, DATE_COLUMN, URL_COLUMN), (sqlite3.Binary(r.content.compressed), r.date, r.url))
                logging.info("Updating '%s' on '%s'" % (r.url, r.date))
        return self.__commit()
