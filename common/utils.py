import re
import json

from post.models import CommentModel


def prepare_json(json_sting):
    if isinstance(json_sting, dict):
        return json_sting

    try:
        return json.loads(json_sting)
    except:
        pass

    return {}


def find_images(body, first=False):
    regex = (r'(https?:\/\/(?:[\da-zA-Z]{1}'
             '(?:[\w\-\.]+\.)+(?:[\w]{2,5}))(?:\:[\d]{1,5})?\/?(?:[^\s\/]+'
             '\/?).*?\.(?:jpe?g|gif|png)(?:\?\w+=\w+(?:\&\w+=\w+)*)?)')

    images = re.findall(regex, body)

    if first:
        return images[0] if images else None

    return images


# TODO Пока не используется, да и нужно ли
# def nodes(node):
#     node['childs'] = []
#
#     for comment in CommentModel.objects(parent_author=node.author,
#                                         parent_permlink=node.permlink):
#
#         node['childs'].append(nodes(comment))
#
#     return node


def find_comments(post):
    comments = []

    for comment in CommentModel.objects(root_comment=post.id):
        if comment.root_comment == comment.id:
            continue

        comments.append(comment)

    return comments
