import re

from models import Comment


def find_images(body, first=False):
    regex = r'\b(https?:\/\/\S+(?:png|jpe?g|gif)\S*)\b'

    images = re.findall(regex, body)

    if first:
        return images[0] if images else None

    return images


def nodes(node):
    node['childs'] = []

    for comment in Comment.objects(parent_author=node.author,
                                   parent_permlink=node.permlink):

        node['childs'].append(nodes(comment))

    return node


def find_comments(post):
    comments = []

    for comment in Comment.objects(parent_author=post.author,
                                   parent_permlink=post.permlink):
        comments.append(nodes(comment))

    return comments
