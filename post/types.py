import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphene.types.generic import GenericScalar
from account.types import Account
from account.models import AccountModel

from post.models import CommentModel, VoteModel
from stats.models import DGPModel

from common.fields import CustomMongoengineConnectionField
from common.utils import find_comments, find_images, prepare_json
from post import utils


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
        return self.get('location', {})


# Отдельный апп
class Vote(MongoengineObjectType):
    voter = graphene.Field(Account)

    def resolve_voter(self, info):
        return AccountModel.objects().get(name=self['voter'])

    class Meta:
        description = '''
            All votes.
        '''
        model = VoteModel
        interfaces = (Node,)


class Post(MongoengineObjectType):
    author = graphene.Field(Account)
    meta = graphene.Field(PostMeta)
    thumb = graphene.String(description='First image in post body')
    total_pending_payout = graphene.Float()
    votes = CustomMongoengineConnectionField(Vote)
    body = graphene.String(linkify_images=graphene.Boolean())
    is_voted = graphene.Boolean(
        description='Check whether the account was voted for this post',
        account=graphene.String(),
    )
    comments = graphene.List('post.types.Post',
                             first=graphene.Int(),
                             last=graphene.Int())

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

    def resolve_is_voted(self, info, account):
        vote = VoteModel.objects(comment=self.id, voter=account).first()

        return vote is not None

    def resolve_comments(self, info, first=None, last=None):
        # TODO Написать простой пагинатор для комментов
        comments = find_comments(self)[::-1]

        if first is not None:
            comments = comments[:first]
        elif last is not None:
            comments = comments[max(0, len(comments) - last):]

        return comments

    def resolve_image(self, info):
        return self.json_metadata['image'][0]

    def resolve_meta(self, info):
        return prepare_json(self.json_metadata)

    def resolve_thumb(self, info):
        return find_images(self.body, first=True)

    def resolve_author(self, info):
        return AccountModel.objects(name=self.author).first()

    def resolve_votes(self, info, args):
        return VoteModel.objects(permlink=self.permlink, author=self.author)

    def resolve_body(self, info, linkify_images=False):
        format = prepare_json(self.json_metadata).get('format', 'html')

        if linkify_images:
            return utils.linkify_images(self.body, format)
        else:
            return self.body


class Comment(Post):
    class Meta:
        description = 'All comments'
        model = CommentModel
        interfaces = (Node,)
