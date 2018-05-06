import os
import json

import datetime as dt

from piston.steem import Steem
from piston.blockchain import Blockchain
from piston.post import Post

from mongostorage import MongoStorage, Indexer


NODE = os.getenv('NODE', 'wss://ws17.golos.io')
OPS = 'comment', 'vote', 'custom_json'

golos = Steem(NODE)
b = Blockchain(steem_instance=golos)

mongo = MongoStorage()
indexer = Indexer(mongo)
start_block = indexer.get_checkpoint('comments')


def update_comment(author, permlink):
    post = Post({'author': author, 'permlink': permlink},
                steem_instance=golos).export()

    if post['depth'] == 0:
        mongo.Posts.update_one(
            {'identifier': post['identifier']},
            {'$set': {**post, 'updatedAt': dt.datetime.utcnow()}}, upsert=True)

    if post['depth'] > 0:
        mongo.Comments.update_one(
            {'identifier': post['identifier']},
            {'$set': {**post, 'updatedAt': dt.datetime.utcnow()}}, upsert=True)


def handle_vote(vote):
    pass


def handle_custom_json(custom_json):
    try:
        meta_str = custom_json.get("json", "{}")
        custom_json['json'] = json.loads(meta_str)
        custom_json['author'] = custom_json.pop('required_posting_auths')[0]
    except Exception as e:
        print('Error', e)
        custom_json['json'] = {"error": "invalid format"}

    if not isinstance(custom_json['json'], (dict, list)):
        custom_json['json'] = {"error": "invalid format"}


for op in b.stream(OPS, start=start_block):
    if op['type'] in ('comment', 'vote'):
        update_comment(op['author'], op['permlink'])
        handle_vote(op)

    if op['type'] == 'custom_json':
        handle_custom_json(op)

    indexer.set_checkpoint('comments', op['block_num'])

    if op['block_num'] % 100 == 0 and op['block_num'] != indexer.get_checkpoint('comments'):
        print('Block #', op['block_num'])
