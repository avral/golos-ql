import os
import logging

from tasks import (
    update_comment,
    handle_vote,
    handle_custom_json
)


from piston.steem import Steem
from piston.blockchain import Blockchain

from mongostorage import MongoStorage, Indexer


NODE = os.getenv('NODE', 'wss://ws17.golos.io')
OPS = 'comment', 'vote', 'custom_json'


golos = Steem(NODE)
mongo = MongoStorage()

b = Blockchain(steem_instance=golos)

indexer = Indexer(mongo)
start_block = indexer.get_checkpoint('comments')


current_block = 0
for op in b.stream(OPS, start=start_block):
    try:
        if op['type'] == 'comment':
            update_comment.delay(op)

        if op['type'] == 'vote':
            handle_vote.delay(op)

        if op['type'] == 'custom_json':
            handle_custom_json.delay(op)

    except Exception as e:
        logging.exception('Err op')

    if op['block_num'] % 10000 == 0 and op['block_num'] != current_block:
        print('Block #', op['block_num'])
        current_block = op['block_num']
