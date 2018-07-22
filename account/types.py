from contextlib import suppress

import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType

from account.models import (
    AccountModel
)

from common.utils import prepare_json


class AccountProfile(graphene.ObjectType):
    profile_image = graphene.String()

    def resolve_profile_image(self, info):
        with suppress(KeyError):
            return self['profile_image']


class AccountMeta(graphene.ObjectType):
    profile = graphene.Field(AccountProfile)

    def resolve_profile(self, info):
        with suppress(KeyError):
            return self['profile']


class Account(MongoengineObjectType):
    meta = graphene.Field(AccountMeta)

    class Meta:
        model = AccountModel
        interfaces = (Node,)

    def resolve_meta(self, info):
        return prepare_json(self.json_metadata)
