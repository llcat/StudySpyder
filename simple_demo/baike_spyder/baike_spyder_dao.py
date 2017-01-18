#coding:utf8
from pymongo import MongoClient

class MongoManager(object):
    def __init__(self):
        self.client = MongoClient()

    def getClient(self, host=None, port=None):
        if host is None and port is None:
            return self.client
        else:
            self.client = MongoClient(host=host, port=port)
        return self.client

    def useDatabase(self, name):
        if self.client is not None:
            return self.client[name]
        else:
            print("db name is None")
            return self.client["test"]

    def workCollection(self, db=None, collection=None):
        db = self.useDatabase(db)
        coll = db[collection]
        return coll




