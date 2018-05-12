import os
import logging
import argparse
import datetime as dt
from time import sleep
from config import APP_TAG

from piston.instance import set_shared_steem_instance

parser = argparse.ArgumentParser()

parser.add_argument("--resync", help="increase output verbosity",
                    action="store_true")

args = parser.parse_args()

from tasks import (
    update_comment,
    handle_vote,
)


from piston.steem import Steem
from piston.blockchain import Blockchain
from piston.post import Post

from mongostorage import MongoStorage, Indexer


NODE = os.getenv('NODE', 'wss://ws17.golos.io')
OPS = 'comment', 'vote', 'custom_json'




golos = Steem(NODE)
set_shared_steem_instance(golos)

mongo = MongoStorage()

b = Blockchain(steem_instance=golos)

if os.getenv('RESYNC', False):
    mongo.reset_db()

indexer = Indexer(mongo)

func = getattr(golos.rpc, "get_discussions_by_created")

params = {
    'limit': 100,
    'select_tags': [APP_TAG],
}

SYNC_DONE = False


def fetch_comments(post):
    for comment in [Post(c) for c in post.get_comments(sort="created")]:

        update_comment(comment)

        # Recursion fetch comment on post
        fetch_comments(comment)


def sync_posts():
    while True:
        params.update({
            'start_author': indexer.get_checkpoint('start_author'),
            'start_permlink': indexer.get_checkpoint('start_permlink'),
        })

        posts = [Post(p) for p in func(params, api='social_network')]

        if len(posts) == 1:
            print('посты закончились на', params)
            indexer.set_checkpoint('start_author', None)
            indexer.set_checkpoint('start_permlink', None)

            return

        if len(posts) == 0:
            logging.warn('Zero posts in request!',
                         indexer.get_checkpoint('start_author'),
                         indexer.get_checkpoint('start_permlink'))

            return

        if params['start_author']:
            posts.pop(0)

        for post in posts:
            print('Sync: ', post.author, post.permlink, post.created)
            if mongo.Posts.find({'author': post.author,
                                 'permlink': post.permlink}).count() > 0:
                print('посты закончились на', post.author, post.permlink)

                indexer.set_checkpoint('start_author', None)
                indexer.set_checkpoint('start_permlink', None)

                return

            update_comment(post)
            fetch_comments(post)

            indexer.set_checkpoint('start_author', post.author)
            indexer.set_checkpoint('start_permlink', post.permlink)

# Посты синкнулись, стримим бч
# TODO Написать атомарную синхронизацию, хранить в монге старт_автор/пермлинк
# Что бы синкнуть все до последнего поста и после этого уже стримить бч


sync_posts()

print('Посты синкнулись')


current_block = 0
for op in b.stream(OPS):
    try:
        if op['type'] == 'comment':
            comment = Post(op)

            if APP_TAG in comment.tags:
                update_comment(comment)

        if op['type'] == 'vote':
            handle_vote(op)

        #if op['type'] == 'custom_json':
        #    handle_custom_json(op)

    except Exception as e:
        logging.exception('Err op')

    if op['block_num'] % 10000 == 0 and op['block_num'] != current_block:
        print('Block #', op['block_num'])
        current_block = op['block_num']
