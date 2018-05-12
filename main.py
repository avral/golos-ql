import os
import json
import logging
from config import APP_TAG
from time import sleep

from piston.instance import set_shared_steem_instance

from tasks import (
    update_comment,
    handle_vote,
)


from piston.steem import Steem
from piston.blockchain import Blockchain
from piston.post import Post
from piston.exceptions import PostDoesNotExist

from mongostorage import MongoStorage, Indexer


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


NODE = os.getenv('NODE', 'wss://ws.golos.io')
OPS = 'comment', 'vote', 'custom_json'


mongo = MongoStorage()
if os.getenv('RESYNC', False):
    mongo.reset_db()

indexer = Indexer(mongo)


def main():
    params = {
        'limit': 100,
        #'select_tags': [APP_TAG],
    }

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
                logging.warn('Zero posts in request! {} {}'.format(
                             indexer.get_checkpoint('start_author'),
                             indexer.get_checkpoint('start_permlink')))

                return

            if params['start_author']:
                posts.pop(0)

            for post in posts:
                try:
                    meta_str = post.get("json_metadata", "{}")
                    post['json_metadata'] = json.loads(meta_str)
                except:
                    post['json_metadata'] = {"error": "invalid format"}
                if not isinstance(post['json_metadata'], dict):
                    post['json_metadata'] = {"error": "invalid format"}

                post["tags"] = []
                if post["depth"] == 0:
                    post["tags"] = post["json_metadata"].get("tags", [])

                    if isinstance(post["tags"], str):
                        post["tags"] = post["tags"].split()

                    if post["parent_permlink"] not in post["tags"]:
                        post["tags"].insert(0, post["parent_permlink"])

                if APP_TAG not in post['tags']:
                    indexer.set_checkpoint('start_author', post.author)
                    indexer.set_checkpoint('start_permlink', post.permlink)
                    continue

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
                update_comment(comment)

            if op['type'] == 'vote':
                handle_vote(op)

            #if op['type'] == 'custom_json':
            #    handle_custom_json(op)

        except PostDoesNotExist:
            pass
        except Exception as e:
            logging.exception('Err op')

        if op['block_num'] % 10000 == 0 and op['block_num'] != current_block:
            print('Block #', op['block_num'])
            current_block = op['block_num']


while True:
    try:
        golos = Steem(NODE)
        set_shared_steem_instance(golos)

        b = Blockchain(steem_instance=golos)

        func = getattr(golos.rpc, "get_discussions_by_created")

        main()
    except KeyboardInterrupt:
        print('Quit..', end="\n")
        exit()
    except:
        logging.exception('Error in parser')
        sleep(3)
