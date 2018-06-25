import graphene
from graphql import GraphQLError

from posts.types import Post, Stats
from models import (
    CommentModel,
)


class Marker(graphene.ObjectType):
    identifier = graphene.String()
    location = graphene.types.generic.GenericScalar()

    def resolve_identifier(self, info):
        return self['identifier']

    def resolve_location(self, info):
        # location = self['json_metadata']['location']

        return self['json_metadata']['location']


class Query(graphene.ObjectType):
    posts = graphene.List(
        Post,
        category=graphene.String(),
        author=graphene.String(),
        page=graphene.Int(),
    )
    markers = graphene.List(
        Marker,
        author=graphene.String(),
        bbox=graphene.JSONString()
    )

    post = graphene.Field(Post, identifier=graphene.String())
    stats = graphene.Field(Stats)

    def resolve_posts(self, info, page=1, author=None, category=None):
        page_size = 10
        offset = (page - 1) * page_size
        q = {
            "depth": 0  # Only posts
        }

        if author:
            q['author'] = author
        if category:
            q['category'] = category

        print(q)

        return list(
           CommentModel.objects(**q)
           .skip(offset)
           .limit(page_size)
           .order_by('-created')
        )
        # return list(
        #    CommentModel.objects(**q)
        #    .skip(offset)
        #    .limit(page_size)
        #    .order_by('-created')
        # )

    def resolve_post(self, context, identifier=None):
        author, permlink = identifier[1:].split('/')

        return CommentModel.objects.get(author=author, permlink=permlink)

    def resolve_stats(self, context):
        return Stats()

    def resolve_markers(self, context, bbox=None, author=None):
        #  Преобразует старый формат в валидные GeoJSON поинты
        # TODO Реализовать поиск по координатам
        # http://docs.mongoengine.org/guide/querying.html#geo-queries
        query = [
            {"$limit": 150},

            {
                "$addFields": {
                    "json_metadata.location": {
                        "$cond": {
                            "if": {
                                "$eq": [{"$type": "$json_metadata.coordinates"}, "string"]
                            },
                            "then": {
                                "name": "$json_metadata.location",
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": {
                                        "$split": [
                                            "$json_metadata.coordinates",
                                            ","
                                        ]
                                    }
                                }
                            },
                            "else": {
                                "name": "$json_metadata.location.name",
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                         "$json_metadata.location.lat",
                                         "$json_metadata.location.lng"
                                     ]
                                }
                            }
                        }
                    }
                }
            }
        ]

        if author:
            query.append({"$match": {"author": author}})

        if bbox:
            if len(bbox) != 4:
                raise GraphQLError('Invalid bbox')

            x0, y0, x1, y1 = bbox
            polygon = [(x0, y0), (x0, y1), (x1, y1), (x1, y0), (x0, y0)]

            {
                "$match": {
                    "json_metadata.location.geometry": {
                        "$geoWithin": {
                            "$geometry": {
                                "type": "Polygon",
                                "coordinates": [polygon]
                            }
                        }
                    }
                }
            }

            #query.append({
            #    "$match": {
            #        "json_metadata.location.geometry": {
            #            "$geoWithin": {
            #                "$box": [(bbox[0], bbox[1]), (bbox[2], bbox[3])]
            #            }
            #        }
            #    }
            #})
        # TODO Не находит точки в азии

        # Лимин на 150 маркеров за 1 раз
        #return list(PostModel.objects.aggregate(*query))[:150]
        return list(CommentModel.objects.aggregate(*query))


schema = graphene.Schema(query=Query, types=[Post, Stats])

        # q = [
        #     {"$match": {"depth": 0}},  # Get only posts
        #     {"$sort": {'created': -1}},

        #     {"$skip": offset},
        #     {"$limit": page_size},
