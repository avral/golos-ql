import os
import graphene
import importlib
from inspect import getmembers, isclass


class QueriesAbstract(graphene.ObjectType):
    pass


queries_base_classes = [QueriesAbstract]
current_directory = os.path.dirname(os.path.abspath(__file__))
current_module = current_directory.split('/')[-1]
subdirectories = [
    x
    for x in os.listdir(current_directory)
    if os.path.isdir(os.path.join(current_directory, x)) and
    x != '__pycache__'
]

for directory in subdirectories:
    try:
        module = importlib.import_module(f'{directory}.queries', package='.')
        if module:
            classes = [x for x in getmembers(module, isclass)]
            queries = [x[1] for x in classes if 'Query' in x[0]]
            queries_base_classes += queries
    except ModuleNotFoundError as e:
        # print(e.msg, directory)
        pass

queries_base_classes = queries_base_classes[::-1]
properties = {}

for base_class in queries_base_classes:
    properties.update(base_class.__dict__['_meta'].fields)

Queries = type(
    'Queries',
    tuple(queries_base_classes),
    properties
)
