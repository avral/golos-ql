import os

import graphene
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from mongoengine import connect

import query


app = Flask(__name__)
app.debug = True
CORS(app)

connect(
    os.getenv('GOLOS_DB_NAME', 'Golos'),
    username=os.getenv('MONGO_USER'),
    password=os.getenv('MONGO_PASSWORD'),
    host=os.getenv('MONGO_HOST', 'localhost'),
    port=int(os.getenv('MONGO_PORT', 27017))
)


schema = graphene.Schema(query=query.Queries)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql',
                                                           schema=schema,
                                                           graphiql=True))

if __name__ == '__main__':
    app.run()
