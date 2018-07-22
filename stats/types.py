import graphene
from graphene.types.generic import GenericScalar

from post.models import CommentModel
from stats.models import DGPModel
# from utils import prepare_json


class Stats(graphene.ObjectType):
    posts_count = graphene.Int()
    dynamic_global_properties = GenericScalar()

    def resolve_posts_count(self, info):
        return CommentModel.objects(depth=0).count()

    def resolve_dynamic_global_properties(self, info):
        # FIXME Расписать все в модели

        d = DGPModel.objects.first().__dict__

        for _ in ["_cls", "_dynamic_lock", "_fields_ordered"]:
                del d[_]

        return d
