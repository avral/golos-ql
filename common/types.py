import graphene
from graphene.types.generic import GenericScalar


class GeometryObjectType(graphene.ObjectType):
    # TODO default_resolver = resolver.geometry_resolver
    type = graphene.String()
    coordinates = GenericScalar()

    def resolve_type(self, info):
        return self.get('type')

    def resolve_coordinates(self, info):
        return self.get('coordinates')
