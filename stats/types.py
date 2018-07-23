import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType

from post.models import CommentModel
from stats.models import DGPModel


class GDB(MongoengineObjectType):
    class Meta:
        description = 'dynamic_global_properties'
        model = DGPModel
        interfaces = (Node,)


class Stats(graphene.ObjectType):
    posts_count = graphene.Int()
    dynamic_global_properties = graphene.Field(GDB)

    def resolve_posts_count(self, info):
        return CommentModel.objects(depth=0).count()

    def resolve_dynamic_global_properties(self, info):
        return DGPModel.objects.first()
