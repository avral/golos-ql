import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphene.types.generic import GenericScalar

from models import (
    Post as PostModel,
    Comment as CommentModel
)
from utils import find_comments, find_images


class Meta(graphene.ObjectType):
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


class Comment(MongoengineObjectType):
    class Meta:
        model = CommentModel
        interfaces = (Node,)


class Stats(graphene.ObjectType):
    posts_count = graphene.Int()

    def resolve_posts_count(self, info):
        return PostModel.objects.count()


class Vote(graphene.ObjectType):
    voter = graphene.String()

    def resolve_voter(self, info):
        return self['voter']


class Post(MongoengineObjectType):
    comments = graphene.List(Comment)
    json_metadata = graphene.Field(Meta)
    thumb = graphene.String()
    active_votes = graphene.List(Vote)

    class Meta:
        model = PostModel
        interfaces = (Node,)

    def resolve_comments(self, info):
        return find_comments(self)

    def resolve_image(self, info):
        return self.json_metadata['image'][0]

    def resolve_json_metadata(self, info):
        return self.json_metadata

    def resolve_thumb(self, info):
        return find_images(self.body, first=True)
