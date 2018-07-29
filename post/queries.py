import os

import graphene

from post.types import Post, Comment
from post.models import CommentModel
from common.fields import CustomMongoengineConnectionField, CommentIdentifier
from post.utils import qs_ab_filter


class PostQuery(graphene.ObjectType):
    posts = CustomMongoengineConnectionField(Post)
    post = graphene.Field(Post, identifier=CommentIdentifier())

    comments = CustomMongoengineConnectionField(Comment)
    comment = graphene.Field(Comment, identifier=graphene.String())

    def resolve_posts(self, info, args):
        qs = CommentModel.objects(depth=0)

        return qs_ab_filter(qs, args)

    def resolve_post(self, context, identifier=None):
        author, permlink = identifier[1:].split('/')

        return CommentModel.objects.get(author=author, permlink=permlink)

    def resolve_comments(self, info, args):
        qs = CommentModel.objects(depth__ne=0)

        return qs_ab_filter(qs, args)

    def resolve_comment(self, context, identifier=None):
        author, permlink = identifier[1:].split('/')

        return CommentModel.objects.get(depth__ne=0,
                                        author=author,
                                        permlink=permlink)
