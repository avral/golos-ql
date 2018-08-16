import graphene

from account.types import Account, AccountAuthority
from account.models import AccountModel, AccountAuthorityModel
from common.fields import CustomMongoengineConnectionField


class AccountQuery(graphene.ObjectType):
    account = graphene.Field(Account, name=graphene.String())
    accounts = CustomMongoengineConnectionField(Account)
    account_authority = graphene.Field(AccountAuthority, account=graphene.String())

    def resolve_accounts(self, info, args):
        return AccountModel.objects()

    def resolve_account(self, info, name):
        return AccountModel.objects(name=name).first()

    def resolve_account_authority(self, info, account):
        return AccountAuthorityModel.objects(account=account).first()
