from mongoengine import DynamicDocument
from mongoengine.fields import (
    StringField, IntField, DateTimeField,
    FloatField
)


class DGPModel(DynamicDocument):
    confidential_sbd_supply_symbol = StringField()
    confidential_sbd_supply_value = IntField()
    confidential_supply_symbol = StringField()
    confidential_supply_value = IntField()
    current_aslot = IntField()
    current_reserve_ratio = IntField()
    current_sbd_supply_symbol = StringField()
    current_sbd_supply_value = FloatField()
    current_supply_symbol = StringField()
    current_supply_value = FloatField()
    current_witness = StringField()
    head_block_id = StringField()
    head_block_number = IntField()
    last_irreversible_block_num = IntField()
    max_virtual_bandwidth = IntField()
    maximum_block_size = IntField()
    num_pow_witnesses = IntField()
    participation_count = IntField()
    recent_slots_filled = IntField()
    sbd_interest_rate = IntField()
    sbd_print_rate = IntField()
    time = DateTimeField()
    total_pow = IntField()
    total_reward_fund_steem_symbol = StringField()
    total_reward_fund_steem_value = FloatField()
    total_reward_shares2 = IntField()
    total_vesting_fund_steem_symbol = StringField()
    total_vesting_fund_steem_value = FloatField()
    total_vesting_shares_symbol = StringField()
    total_vesting_shares_value = FloatField()
    virtual_supply_symbol = StringField()
    virtual_supply_value = FloatField()
    vote_regeneration_per_day = IntField()

    meta = {'collection': 'dynamic_global_property_object'}
