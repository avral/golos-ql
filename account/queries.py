import graphene

from account.types import Account, AccountAuthority
from account.models import AccountModel, AccountAuthorityModel
from common.fields import CustomMongoengineConnectionField


class AccountMetaFilterInput(graphene.InputObjectType):
    not_null = graphene.String()


class AccountQuery(graphene.ObjectType):
    account = graphene.Field(Account, name=graphene.String())
    accounts = CustomMongoengineConnectionField(Account,
                                                meta=AccountMetaFilterInput())

    account_authority = graphene.Field(AccountAuthority,
                                       account=graphene.String())

    def resolve_accounts(self, info, args):
        qs = AccountModel.objects()

        meta = args.get('meta', {})
        not_null = meta.get('not_null')

        if not_null:
            qs = qs.filter(
                __raw__={f'json_metadata.{not_null}': {'$exists': True}}
            )

        return qs

    def resolve_account(self, info, name):
        return AccountModel.objects(name=name).first()

    def resolve_account_authority(self, info, account):
        return AccountAuthorityModel.objects(account=account).first()
