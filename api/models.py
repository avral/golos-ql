import os

from mongoengine import Document, DynamicDocument, connect
from mongoengine.fields import (
    StringField, ObjectId, IntField, DictField,
    DateTimeField, ListField
)


DB_NAME = os.getenv('DB_NAME', 'mapala')
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')

connect(DB_NAME, host=MONGO_HOST)


class Post(DynamicDocument):
    author = StringField()
    active_votes = DictField()
    children = IntField()
    title = StringField()
    identifier = StringField()
    body = StringField()
    json_metadata = DictField()
    permlink = StringField()
    created = DateTimeField()
    meta = {'collection': 'Posts'}


class Comment(DynamicDocument):
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
    meta = {'collection': 'Comments'}


class Indexer(Document):
    meta = {'collection': '_indexer'}
    _id = ObjectId()
    operations_checkpoint = IntField()
    start_author_checkpoint = StringField()
    start_permlink_checkpoint = StringField()
