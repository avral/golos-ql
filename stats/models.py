from mongoengine import DynamicDocument
from mongoengine.fields import (
    StringField, IntField, DictField,
    DateTimeField, ObjectId
)


class DGPModel(DynamicDocument):
    average_block_size = IntField()

    meta = {'collection': 'dynamic_global_property_object'}
