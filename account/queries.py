import graphene

from account.types import Account
from account.models import AccountModel


class AccountQuery(graphene.ObjectType):
    account = graphene.Field(Account, name=graphene.String())

    def resolve_account(self, info, name):
        return AccountModel.objects(name=name).first()
