import graphene

from stats.types import Stats


class StatsQuery(graphene.ObjectType):
    stats = graphene.Field(Stats)

    def resolve_stats(self, context):
        return Stats()
