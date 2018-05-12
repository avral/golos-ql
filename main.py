import os
import json
import logging
from time import sleep

from tqdm import tqdm
from piston.instance import set_shared_steem_instance
from pistonapi.steemnoderpc import SteemNodeRPC

from tasks import (
    update_comment,
    handle_vote,
)


from piston.steem import Steem
from piston.blockchain import Blockchain

from mongostorage import MongoStorage, Indexer


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


NODE = os.getenv('NODE', 'wss://ws17.golos.io')
OPS = 'comment', 'vote', 'custom_json'


# HACK Патчим на ошибки от ноды, что бы скрипт не падал
def _rpcexec(self, *args, **kwargs):
    try:
        return super(SteemNodeRPC, self).rpcexec(*args, **kwargs)
    except Exception as e:
        logging.warning(f'Node rpc error: {e}')
        sleep(3)

        return _rpcexec(self, *args, **kwargs)


SteemNodeRPC.rpcexec = _rpcexec

golos = Steem(NODE)
set_shared_steem_instance(golos)

mongo = MongoStorage()
indexer = Indexer(mongo)


def sync_init_posts():
    with open('mapala_all_posts_13.05.json') as f:
        for post_identifi in tqdm(json.load(f), 'Sync init posts'):
            update_comment(post_identifi)

        indexer.set_status('init_posts_synced', True)
        logging.info('Init sync complete.')


def stream():
    current_block = 0
    for op in Blockchain().stream(OPS):
        try:
            if op['type'] == 'comment':
                update_comment(op)

            if op['type'] == 'vote':
                handle_vote(op)
        except Exception as e:
            logging.exception('Err op')

        if op['block_num'] % 100 == 0 and op['block_num'] != current_block:
            logging.info('Block # %s' % op['block_num'])
            current_block = op['block_num']


def main():
    if indexer.get_status('init_posts_synced') is False:
        sync_init_posts()

    stream()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Quit..', end="\n")
        exit()
    except:
        logging.exception('Error init parser')
