import os

import pymongo
from pymongo.errors import ConnectionFailure

MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', 27017)

DB_NAME = os.getenv('DB_NAME', 'mapala')


class MongoStorage(object):
    def __init__(self, db_name=DB_NAME, host=MONGO_HOST, port=MONGO_PORT):
        try:
            mongo_url = 'mongodb://%s:%s/%s' % (host, port, db_name)
            client = pymongo.MongoClient(mongo_url)
            self.db = client[db_name]

        except ConnectionFailure as e:
            print('Can not connect to MongoDB server: %s' % e)
            raise
        else:
            self.Accounts = self.db['Accounts']
            self.Posts = self.db['Posts']
            self.Comments = self.db['Comments']
            self.CustomJson = self.db['CustomJson']
            self.Test = self.db['Test']

    def list_collections(self):
        return self.db.collection_names()

    def reset_db(self):
        for col in self.list_collections():
            self.db.drop_collection(col)

    def ensure_indexes(self):
        self.Posts.create_index([('author', 1), ('permlink', 1)], unique=True)
        self.Posts.create_index([('identifier', 1)], unique=True)
        self.Posts.create_index([('author', 1)])
        self.Posts.create_index([('created', -1)])
        self.Posts.create_index([('json_metadata.app', 1)], background=True, sparse=True)
        self.Posts.create_index([('json_metadata.users', 1)], background=True, sparse=True)
        self.Posts.create_index([('json_metadata.tags', 1)], background=True, sparse=True)
        self.Posts.create_index([('json_metadata.community', 1)], background=True, sparse=True)
        self.Posts.create_index([('json_metadata.location', 1)], background=True, sparse=True)
        self.Posts.create_index([('json_metadata.location.lng', 1)], background=True, sparse=True)
        self.Posts.create_index([('json_metadata.location.lat', 1)], background=True, sparse=True)
        self.Posts.create_index([('body', 'text'), ('title', 'text')], background=True)

        self.Comments.create_index([('identifier', 1)], unique=True)
        self.Comments.create_index([('parent_author', 1)])
        self.Comments.create_index([('parent_permlink', 1)])
        self.Comments.create_index([('author', 1)])
        self.Comments.create_index([('permlink', 1)])
        self.Comments.create_index([('created', -1)])
        self.Comments.create_index([('body', 'text'), ('title', 'text')], background=True)

        self.CustomJson.create_index([('id', 1)])
        self.CustomJson.create_index([('timestamp', -1)])
        self.CustomJson.create_index([('json', 1)], background=True, sparse=True)
        self.CustomJson.create_index([('author', 1)], background=True, sparse=True)

        # 4 jesta's tools
        self.Operations.create_index(
            [('producer', 1), ('type', 1), ('timestamp', 1)],
            sparse=True, background=True)
        self.Operations.create_index(
            [('curator', 1), ('type', 1), ('timestamp', 1)],
            sparse=True, background=True)
        self.Operations.create_index(
            [('benefactor', 1), ('type', 1), ('timestamp', 1)],
            sparse=True, background=True)
        self.Operations.create_index(
            [('author', 1), ('type', 1), ('timestamp', 1)],
            sparse=True, background=True)


class Indexer(object):
    def __init__(self, mongo):
        self.coll = mongo.db['_indexer']
        self.instance = self.coll.find_one()

        if not self.instance:
            self.coll.insert_one({
                "operations_checkpoint": 1,
                "start_author_checkpoint": None,
                "start_permlink_checkpoint": None
            })

            self.instance = self.coll.find_one()

    def get_checkpoint(self, name):
        field = f'{name}_checkpoint'
        return self.coll.find_one().get(field)

    def set_checkpoint(self, name, index):
        field = f'{name}_checkpoint'
        return self.coll.update_one({}, {"$set": {field: index}})


class Stats(object):
    def __init__(self, mongo):
        self.mongo = mongo
        self._stats = mongo.db['stats']
        self.stats = self._stats.find_one()
