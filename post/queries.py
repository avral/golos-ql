import graphene

from post.types import Post, Comment
from post.models import CommentModel
from common.fields import CustomMongoengineConnectionField, CommentIdentifier
from post.utils import qs_ab_filter


class Geometry(graphene.InputObjectType):
    type = graphene.String()
    coordinates = graphene.List(graphene.Float)


class PostOrderingEnum(graphene.Enum):
    created_ASC = '-created'
    created_DESC = 'created'
    total_payout_value_ASC = '-total_payout_value'
    total_payout_value_DESC = 'total_payout_value'


class MetaFilterInput(graphene.InputObjectType):
    tags = graphene.List(graphene.String)
    app = graphene.String()
    # TODO Разобраться с фильтрацией location = Geometry()


class PostQuery(graphene.ObjectType):
    post = graphene.Field(Post, identifier=CommentIdentifier())
    posts = CustomMongoengineConnectionField(Post,
                                             meta=MetaFilterInput(),
                                             orderBy=PostOrderingEnum())

    comments = CustomMongoengineConnectionField(Comment)
    comment = graphene.Field(Comment, identifier=graphene.String())

    def resolve_posts(self, info, args):
        qs = CommentModel.objects(depth=0, removed=False)

        meta = args.get('meta', {})

        if 'orderBy' in args:
            qs = qs.order_by(args['orderBy'])

        tags = meta.get('tags')
        app = meta.get('app')

        if tags:
            qs = qs.filter(json_metadata__tags__all=tags)

        if app:
            qs = qs.filter(json_metadata__app=app)

        return qs_ab_filter(qs, args)

    def resolve_post(self, context, identifier=None):
        author, permlink = identifier[1:].split('/')

        return CommentModel.objects(author=author, permlink=permlink).first()

    def resolve_comments(self, info, args):
        qs = CommentModel.objects(depth__ne=0, removed=False)

        return qs_ab_filter(qs, args)

    def resolve_comment(self, context, identifier=None):
        author, permlink = identifier[1:].split('/')

        return CommentModel.objects(depth__ne=0,
                                    author=author,
                                    permlink=permlink).first()
