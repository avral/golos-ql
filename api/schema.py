import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from utils import find_comments
from graphene.types.generic import GenericScalar

from models import (
    Post as PostModel,
    Comment as CommentModel
)


class Meta(graphene.ObjectType):
    image = GenericScalar(first=graphene.Boolean())
    app = GenericScalar()
    location = GenericScalar()

    def resolve_image(self, info, first=False):
        images = self.get('image', [])

        if images:
            return images[0] if first else images

        return []

    def resolve_app(self, info):
        return self.get('app', 'undefined')

    def resolve_location(self, info):
        return self.get('location')


class Comment(MongoengineObjectType):
    class Meta:
        model = CommentModel
        interfaces = (Node,)


class Post(MongoengineObjectType):
    comments = graphene.List(Comment)
    json_metadata = graphene.Field(Meta)

    class Meta:
        model = PostModel
        interfaces = (Node,)

    def resolve_comments(self, info):
        return find_comments(self)

    def resolve_image(self, info):
        return self.json_metadata['image'][0]

    def resolve_json_metadata(self, info):
        return self.json_metadata


class Query(graphene.ObjectType):
    posts = graphene.List(
        Post,
        author=graphene.String(),
        page=graphene.Int(),
        bbox=graphene.JSONString()
    )

    post = graphene.Field(Post, identifier=graphene.String())
    markers = graphene.Field(Post, identifier=graphene.String())

    def resolve_posts(self, info, page=1, author=None, bbox={}):
        # TODO Реализовать поиск по координатам
        # http://docs.mongoengine.org/guide/querying.html#geo-queries
        q = {}

        if author:
            q['author'] = author

        page_size = 10
        offset = (page - 1) * page_size

        return list(PostModel.objects(**q).skip(offset).limit(page_size))

    def resolve_post(self, context, identifier=None):
        return PostModel.objects.get(identifier=identifier)


schema = graphene.Schema(query=Query, types=[Post])
