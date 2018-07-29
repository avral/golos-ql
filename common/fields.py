import graphene

from graphene_mongo import MongoengineConnectionField
from graphene_mongo.converter import convert_mongoengine_field
from graphene_mongo.utils import get_model_fields


class CustomMongoengineConnectionField(MongoengineConnectionField):
    @property
    def fields(self):
        return self.type._meta.fields

    @property
    def field_args(self):
        args = {}

        # TODO Depth убрать Или сделать поля для фильтров
        for k, v in get_model_fields(self.model).items():
            if k in self.model._meta['indexes']:
                v.null = True
                args[k] = convert_mongoengine_field(v)

        return args

    @classmethod
    def connection_resolver(cls, resolver, connection, model, root, info, **args):
        qs = resolver(root, info, args)

        qs = qs.filter(**{
            key: value
            for key, value in args.copy().items()
            if key in model._meta['indexes'] and key in args.keys()
        })

        first = args.pop('first', None)
        last = args.pop('last', None)
        before = args.pop('before', None)
        after = args.pop('after', None)

        if after is not None or before is not None:
            # FIX Пока нет нормальных полей в монге
            # raise NotImplementedError('Handle after/before in root resolver')
            pass

        if first is not None:
            qs = qs[:first]
        if last is not None:
            qs = qs[max(0, qs.count() - last):]

        edges = [connection.Edge(node=node, cursor=node.id) for node in qs]

        return connection(edges=edges)


class CommentIdentifier(graphene.String):
    """
    Comment unicue ID (str)``@<author>/<permlink>``
    """
