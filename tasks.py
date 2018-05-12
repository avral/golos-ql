import os
import logging
import datetime as dt
from celery import Celery
from piston.post import Post
import json
from piston.steem import Steem
from mongostorage import MongoStorage, Indexer
from config import APP_TAG
from contextlib import suppress


app = Celery(
    'tasks',
    backend=os.getenv('CELERY_BACKEND_URL', 'redis://localhost:6379/0'),
    broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
)

BLOCK_FROM_UPDATE_COMMENT_BY_VOTE = \
        os.getenv('BLOCK_FROM_UPDATE_COMMENT_BY_VOTE', 16_000_000)


NODE = os.getenv('NODE', 'wss://ws17.golos.io')
golos = Steem(NODE)
mongo = MongoStorage()
indexer = Indexer(mongo)


#@app.task(ignore_result=True)
def update_comment(comment):
    if not isinstance(comment, object):
        comment = Post(comment)

    if not comment.is_comment():
        comment = comment.export()

        if APP_TAG not in comment['tags']:
            return

        mongo.Posts.update_one(
            {'identifier': comment['identifier']},
            {'$set': {**comment, 'updatedAt': dt.datetime.utcnow()}},
            upsert=True)

        logging.info(f'Sync: {comment["author"]} {comment["permlink"]}')
    else:
        parent_q = {
            'author': comment.parent_author,
            'permlink': comment.parent_permlink
        }

        # TODO Один запрос
        if (mongo.Posts.find(parent_q).count() > 0 or
                mongo.Comments.find(parent_q).count() > 0):

            comment = comment.export()

            mongo.Comments.update_one(
                {'identifier': comment['identifier']},
                {'$set': {**comment, 'updatedAt': dt.datetime.utcnow()}},
                upsert=True)

            logging.info(f'Sync: {comment["author"]} {comment["permlink"]}')

#@app.task(ignore_result=True)
def handle_vote(vote):
    comment_for_update = Post({'author': vote['author'],
                               'permlink': vote['permlink']})

    update_comment(comment_for_update)

    # TODO Обработака апвоутов


@app.task(ignore_result=True)
def handle_custom_json(custom_json):
    try:
        meta_str = custom_json.get("json", "{}")
        custom_json['json'] = json.loads(meta_str)
        custom_json['author'] = custom_json.pop('required_posting_auths')[0]
    except Exception as e:
        logging.exception('Error', e)
        custom_json['json'] = {"error": "invalid format"}

    if not isinstance(custom_json['json'], (dict, list)):
        custom_json['json'] = {"error": "invalid format"}

    mongo.CustomJson.insert_one(custom_json)
