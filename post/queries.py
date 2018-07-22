import os

import graphene

from post.types import Post, Comment
from post.models import CommentModel


class PostQuery(graphene.ObjectType):
    posts = graphene.List(
        Post,
        # tag=graphene.String(),
        category=graphene.String(),
        author=graphene.String(),
        page=graphene.Int(),
    )

    post = graphene.Field(Post, identifier=graphene.String())

    comments = graphene.List(
        Comment,
        page=graphene.Int(),
    )

    comment = graphene.Field(Comment, identifier=graphene.String())

    # TODO Набистать абстрактную пагинацию и фильтрацию
    def resolve_posts(self, info, page=1,
                      author=None, category=None, tag=None):
        # {"tags":\[.*"ru--golos".*?\],
        page_size = int(os.getenv('PAGINATION', 10))
        offset = (page - 1) * page_size
        q = {
            "depth": 0  # Only posts
        }

        if author:
            q['author'] = author
        if category:
            q['category'] = category
        # if tag:
        #     q['json_metadata__contains'] = r'{"tags":\[.*"%s".*?\],' % tag

        return list(
           CommentModel.objects(**q)
           .skip(offset)
           .limit(page_size)
        )

    def resolve_post(self, context, identifier=None):
        author, permlink = identifier[1:].split('/')

        return CommentModel.objects.get(author=author, permlink=permlink)

    def resolve_comments(self, info, page=1):
        page_size = int(os.getenv('PAGINATION', 10))
        offset = (page - 1) * page_size

        return list(
           CommentModel.objects(depth__ne=0)
           .skip(offset)
           .limit(page_size)
        )

    def resolve_comment(self, context, identifier=None):
        author, permlink = identifier[1:].split('/')

        return CommentModel.objects.get(depth__ne=0,
                                        author=author,
                                        permlink=permlink)
