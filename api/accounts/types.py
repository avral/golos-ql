import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphene.types.generic import GenericScalar

from models import (
    AccountModel
)

from utils import prepare_json


class Meta(graphene.ObjectType):
    image = GenericScalar(first=graphene.Boolean())
    app = GenericScalar()
    location = GenericScalar()
    tags = GenericScalar()
    format = graphene.String()


class Account(MongoengineObjectType):
    class Meta:
        model = AccountModel
        interfaces = (Node,)

    def resolve_json_metadata(self, info):
        return prepare_json(self.json_metadata)
