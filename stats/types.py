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


class BlockChain(graphene.ObjectType):
    dynamic_global_properties = graphene.Field(GDB)

    def resolve_dynamic_global_properties(self, info):
        return DGPModel.objects.first()


class PostStats(graphene.ObjectType):
    posts_count = graphene.Int()
    total_payout = graphene.Int(category=graphene.String())

    def resolve_posts_count(self, info):
        return CommentModel.objects(depth=0).count()

    def resolve_total_payout(self, info, category=None):
        qs = CommentModel.objects(depth=0)

        if category:
            qs = qs.filter(category=category)

        return qs.sum('total_payout_value')


class Stats(graphene.ObjectType):
    blockchain = graphene.Field(BlockChain)
    posts = graphene.Field(PostStats)

    def resolve_posts(self, info):
        return PostStats()

    def resolve_blockchain(self, info):
        return BlockChain()
