import os

from mongoengine import Document, DynamicDocument, connect
from mongoengine.fields import (
    StringField, ObjectId, IntField, DictField,
    DateTimeField
)


DB_NAME = os.getenv('DB_NAME', 'Golos')
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', 27017)


connect(DB_NAME, host=MONGO_HOST, port=int(MONGO_PORT))


class AccountModel(DynamicDocument):
    name = StringField()
    json_metadata = DictField()

    meta = {'collection': 'account_object'}


class CommentModel(DynamicDocument):
    author = StringField()
    active_votes = DictField()
    children = IntField()
    title = StringField()
    identifier = StringField()
    body = StringField()
    json_metadata = DictField()
    permlink = StringField()
    depth = IntField()
    created = DateTimeField()

    meta = {'collection': 'comment_object'}
