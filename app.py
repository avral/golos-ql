import os

from flask import Flask
from flask_graphql import GraphQLView
from flask_graphql import render_graphiql
from flask_cors import CORS

import graphene
from mongoengine import connect
from raven.contrib.flask import Sentry

import query


with open('./playground_template.html', 'r') as myfile:
    render_graphiql.TEMPLATE = myfile.read()

app = Flask(__name__)
app.debug = True
CORS(app)
Sentry(app)

connect(
    os.getenv('GOLOS_DB_NAME', 'Golos'),
    username=os.getenv('MONGO_USER'),
    password=os.getenv('MONGO_PASSWORD'),
    host=os.getenv('MONGO_HOST', 'localhost'),
    port=int(os.getenv('MONGO_PORT', 27017))
)


# TODO Default query
default_query = """
{
  post(identifier: "@avral/ru-golos-ql-anons-graphql-servera-dlya-golosa") {
    title,
    body,
    thumb,
    comments(last: 2) {
      body,
      created,
      parentAuthor,
      parentPermlink,
      author {
        name
      }
    },
    isVoted(account: "seriy"),
    netVotes,
    author {
      name,
      balanceValue,
      meta {
        profile {
          profileImage
        }
      }
    },
    votes(first: 10) {
      edges {
        node {
          voter {
            name,
          }
        }
      }
    }
  }
}
""".strip()


schema = graphene.Schema(query=query.Queries)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql',
                                                           schema=schema,
                                                           graphiql=True,
                                                           query=default_query))

if __name__ == '__main__':
    app.run()
