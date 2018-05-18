import os
import json
import logging
import datetime as dt
from piston.post import Post
from piston.exceptions import PostDoesNotExist
from mongostorage import MongoStorage, Indexer
from config import APP_TAG
from contextlib import suppress


NODE = os.getenv('NODE', 'wss://ws17.golos.io')
mongo = MongoStorage()
indexer = Indexer(mongo)


def fetch_comments(post):
    for comment in [c for c in post.get_comments(sort="created")]:
        update_comment(comment)

        with suppress(PostDoesNotExist):
            fetch_comments(Post(comment))


def add_comm(comm):
    comment = comm.export()

    mongo.Comments.update_one(
        {'identifier': comment['identifier']},
        {'$set': {**comment, 'updatedAt': dt.datetime.utcnow()}},
        upsert=True)

    logging.info(f'Sync: {comm.author} {comm.permlink}')


def add_post(comm):
    post = comm.export()

    mongo.Posts.update_one(
        {'identifier': post['identifier']},
        {'$set': {**post, 'updatedAt': dt.datetime.utcnow()}},
        upsert=True)

    if indexer.get_status('init_posts_synced') is False:
        fetch_comments(comm)

    logging.info(f'Sync: {comm.author} {comm.permlink}')


def update_comment(comment):
    if not isinstance(comment, Post):
        try:
            comment = Post(comment)
            comment.refresh()
        except PostDoesNotExist:
            return

    if not comment.is_comment():
        print(comment, comment.tags, APP_TAG)
        if APP_TAG not in comment.tags:
            return

        add_post(comment)

    else:
        parent_q = {
            'author': comment.parent_author,
            'permlink': comment.parent_permlink
        }

        # TODO Один запрос
        if (mongo.Posts.find(parent_q).count() > 0 or
                mongo.Comments.find(parent_q).count() > 0):

            add_comm(comment)


def handle_vote(vote):
    update_comment(f'@{vote["author"]}/{vote["permlink"]}')

    # TODO Обработака апвоутов


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
