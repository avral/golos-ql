import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphene.types.generic import GenericScalar
from account.types import Account
from account.models import AccountModel

from post.models import CommentModel, VoteModel
from stats.models import DGPModel

from common.utils import find_comments, find_images, prepare_json


class PostMeta(graphene.ObjectType):
    image = GenericScalar(first=graphene.Boolean())
    app = GenericScalar()
    location = GenericScalar()
    tags = GenericScalar()
    format = graphene.String()

    def resolve_format(self, info):
        return self.get('format', None)

    def resolve_tags(self, info):
        return self.get('tags', [])

    def resolve_image(self, info, first=False):
        images = self.get('image', [])

        if images:
            return images[0] if first else images

        return []

    def resolve_app(self, info):
        return self.get('app', 'undefined')

    def resolve_location(self, info):
        return self.get('location')


# Отдельный апп
class Vote(graphene.ObjectType):
    voter = graphene.String()

    def resolve_voter(self, info):
        return self['voter']


class Post(MongoengineObjectType):
    comments = graphene.List('post.types.Post')
    author = graphene.Field(Account)
    json_metadata = graphene.Field(PostMeta)
    thumb = graphene.String(description='First image in post body')
    total_payout = graphene.Int()
    total_pending_payout = graphene.Float()
    is_voted = graphene.Boolean(
        description='Check whether the account was voted for this post',
        account=graphene.String(),
    )

    class Meta:
        description = '''
            All posts.
            Pagination - posts is divided into pages,
            use page param: page=2
        '''
        model = CommentModel
        interfaces = (Node,)

    def resolve_total_pending_payout(self, info):
        dgp = DGPModel.objects.first()

        tpp = self['vote_rshares']
        tpp *= dgp.total_reward_fund_steem_value
        tpp /= dgp.total_reward_shares2

        return tpp

    def resolve_total_payout(self, info):
        return 0

    def resolve_is_voted(self, info, account):
        vote = VoteModel.objects(comment=self.id, voter=account).first()

        return vote is not None

    def resolve_comments(self, info):
        return find_comments(self)

    def resolve_image(self, info):
        return self.json_metadata['image'][0]

    def resolve_json_metadata(self, info):
        return prepare_json(self.json_metadata)

    def resolve_thumb(self, info):
        return find_images(self.body, first=True)

    def resolve_author(self, info):
        return AccountModel.objects(name=self.author).first()


class Comment(Post):
    class Meta:
        description = 'All comments'
        model = CommentModel
        interfaces = (Node,)
