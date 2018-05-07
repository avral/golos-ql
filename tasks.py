import os
import datetime as dt
from celery import Celery
from piston.post import Post
import json
from piston.steem import Steem
from mongostorage import MongoStorage, Indexer


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


@app.task(ignore_result=True)
def update_comment(op):
    post = Post({'author': op['author'], 'permlink': op['permlink']},
                steem_instance=golos).export()

    if post['depth'] == 0:
        mongo.Posts.update_one(
            {'identifier': post['identifier']},
            {'$set': {**post, 'updatedAt': dt.datetime.utcnow()}}, upsert=True)

    if post['depth'] > 0:
        mongo.Comments.update_one(
            {'identifier': post['identifier']},
            {'$set': {**post, 'updatedAt': dt.datetime.utcnow()}}, upsert=True)

    indexer.set_checkpoint('comments', op['block_num'])


@app.task(ignore_result=True)
def handle_vote(vote):
    if BLOCK_FROM_UPDATE_COMMENT_BY_VOTE < vote['block_num']:
        # Обновлять посты по апвоуту, начиная с блока
        # что бы не синкать все с начала блокчейна
        update_comment.delay(vote)

    # TODO Обработака апвоутов


@app.task(ignore_result=True)
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

    mongo.CustomJson.insert_one(custom_json)
