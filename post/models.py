from mongoengine import DynamicDocument
from mongoengine.fields import (
    StringField, IntField, DictField,
    DateTimeField, ObjectId, FloatField,
    BooleanField
)


class VoteModel(DynamicDocument):
    author = StringField()
    voter = StringField()
    comment = ObjectId()

    meta = {
        'collection': 'comment_vote_object',
        'indexes': [
            'author',
            'voter',
            'comment',
            'permlink',
            'last_update'
        ],

        'auto_create_index': True,
        'index_background': True
    }


class CommentModel(DynamicDocument):
    abs_rshares = IntField()
    active = DateTimeField()
    allow_curation_rewards = BooleanField()
    allow_replies = BooleanField()
    allow_votes = BooleanField()
    active_votes = DictField()
    author = StringField()
    author_rewards = IntField()
    beneficiary_payout_symbol = StringField()
    beneficiary_payout_value = FloatField()
    body = StringField()
    cashout_time = DateTimeField()
    category = StringField()
    children = IntField()
    children_abs_rshares = IntField()
    children_rshares2 = IntField()
    created = DateTimeField()
    curator_payout_symbol = StringField()
    curator_payout_value = FloatField()
    depth = IntField()
    json_metadata = StringField()
    last_payout = DateTimeField()
    last_update = DateTimeField()
    max_accepted_payout_symbol = StringField()
    max_accepted_payout_value = FloatField()
    max_cashout_time = DateTimeField()
    mode = StringField()
    net_rshares = IntField()
    net_votes = IntField()
    parent_author = StringField()
    parent_permlink = StringField()
    percent_steem_dollars = IntField()
    permlink = StringField()
    removed = BooleanField()
    reward_weight = IntField()
    root_comment = ObjectId()
    title = StringField()
    total_payout_symbol = StringField()
    total_payout_value = FloatField()
    total_vote_weight = IntField()
    vote_rshares = IntField()

    meta = {
        'collection': 'comment_object',
        'ordering': ['-created'],

        'indexes': [
            'author',
            'permlink',
            'created',
            'category',
            'depth',
            'root_comment',
            'parent_permlink',
            'parent_author',
            'mode'
        ],

        'auto_create_index': True,
        'index_background': True
    }
