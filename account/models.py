from mongoengine import DynamicDocument
from mongoengine.fields import (
    StringField, IntField, DateTimeField, BooleanField,
    FloatField, ListField
)


class AccountModel(DynamicDocument):
    active_challenged = BooleanField()
    balance_symbol = StringField()
    balance_value = FloatField()
    can_vote = BooleanField()
    comment_count = IntField()
    created = DateTimeField()
    curation_rewards = IntField()
    delegated_vesting_shares_symbol = StringField()
    delegated_vesting_shares_value = FloatField()
    json_metadata = StringField()
    last_account_recovery = DateTimeField()
    last_account_update = DateTimeField()
    last_active_proved = DateTimeField()
    last_owner_proved = DateTimeField()
    last_post = DateTimeField()
    last_vote_time = DateTimeField()
    lifetime_vote_count = IntField()
    memo_key = StringField()
    mined = BooleanField()
    name = StringField()
    next_vesting_withdrawal = DateTimeField()
    owner_challenged = BooleanField()
    post_count = IntField()
    posting_rewards = IntField()
    roxied_vsf_votes = ListField(StringField())
    proxy = StringField()
    received_vesting_shares_symbol = StringField()
    received_vesting_shares_value = FloatField()
    recovery_account = StringField()
    reset_account = StringField()
    savings_balance_symbol = StringField()
    savings_balance_value = FloatField()
    savings_sbd_balance_symbol = StringField()
    savings_sbd_balance_value = FloatField()
    savings_sbd_last_interest_payment = DateTimeField()
    savings_sbd_seconds = IntField()
    savings_sbd_seconds_last_update = DateTimeField()
    savings_withdraw_requests = IntField()
    sbd_balance_symbol = StringField()
    sbd_balance_value = FloatField()
    sbd_last_interest_payment = DateTimeField()
    sbd_seconds = IntField()
    sbd_seconds_last_update = DateTimeField()
    to_withdraw = IntField()
    vesting_shares_symbol = StringField()
    vesting_shares_value = FloatField()
    vesting_withdraw_rate_symbol = StringField()
    vesting_withdraw_rate_value = FloatField()
    voting_power = IntField()
    withdraw_routes = IntField()
    withdrawn = IntField()
    witnesses_voted_for = IntField()

    meta = {
        'collection': 'account_object',
        'indexes': [
            'name'
        ],

        'auto_create_index': True,
        'index_background': True
    }
