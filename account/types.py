from contextlib import suppress

from mongoengine.base.datastructures import BaseDict
import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphene.types.generic import GenericScalar

from account.models import (
    AccountModel,
    AccountAuthorityModel
)

from common.utils import prepare_json


class AccountProfile(graphene.ObjectType):
    profile_image = graphene.String()
    website = graphene.String()
    cover_image = graphene.String()

    def resolve_cover_image(self, info):
        with suppress(KeyError):
            return self['cover_image']

    def resolve_website(self, info):
        with suppress(KeyError):
            return self['website']

    def resolve_profile_image(self, info):
        with suppress(KeyError):
            return self['profile_image']


class AccountMeta(graphene.ObjectType):
    profile = graphene.Field(AccountProfile)

    def resolve_profile(self, info):
        return self.get('profile', {})


class Account(MongoengineObjectType):
    meta = graphene.Field(AccountMeta)
    json_metadata = GenericScalar()

    def resolve_json_metadata(self, info):
        return prepare_json(self.json_metadata)

    class Meta:
        model = AccountModel
        interfaces = (Node,)

    def resolve_meta(self, info):
        if isinstance(self.json_metadata, BaseDict):
            return self.json_metadata
        else:
            return {}


class AccountAuthority(MongoengineObjectType):
    class Meta:
        model = AccountAuthorityModel
        interfaces = (Node,)
