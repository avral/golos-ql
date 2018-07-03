import os

from pymongo.change_stream import ChangeStream
from mongoengine import Document, DynamicDocument, connect
from mongoengine.fields import (
    StringField, ObjectId, IntField, DictField,
    DateTimeField,
)


DB_NAME = os.getenv('DB_NAME', 'Golos')
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', 27017)


db = connect(DB_NAME, host=MONGO_HOST, port=int(MONGO_PORT))


#
# comment_object = db.Golos.comment_object
#
#
#
# for i in comment_object.watch():
#    print(i)
#


class VoteModel(DynamicDocument):
    author = StringField()
    voter = StringField()
    comment = ObjectId()

    meta = {
        'collection': 'comment_vote_object',
        'indexes': [
            'author',
            'voter',
            'comment'
        ],

        'auto_create_index': True,
        'index_background': True
    }


class AccountModel(DynamicDocument):
    name = StringField()
    json_metadata = DictField()

    meta = {
        'collection': 'account_object',
        'indexes': [
            'name'
        ],

        'auto_create_index': True,
        'index_background': True
    }


class CommentModel(DynamicDocument):
    author = StringField()
    active_votes = DictField()
    children = IntField()
    title = StringField()
    category = StringField()
    body = StringField()
    json_metadata = DictField()
    permlink = StringField()
    depth = IntField()
    created = DateTimeField()
    net_votes = IntField()
    children = IntField()

    meta = {
        'collection': 'comment_object',
        'ordering': ['-created'],

        'indexes': [
            'author',
            'permlink',
            'created',
            'category'
        ],

        'auto_create_index': True,
        'index_background': True
    }
