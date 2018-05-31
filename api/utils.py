import re

from models import Comment


def find_images(body, first=False):
    # FIXME Доработать для маркдауна
    # http://localhost:3000/@nameless-berk/vysokie-gory-glubokie-ushchelxya-i-yeffektnyie-vodopady-tungurahua-baos
    regex = r'((?:https?\:\/\/)(?:[a-zA-Z]{1}(?:[\w\-]+\.)+(?:[\w]{2,5}))' \
            '(?:\:[\d]{1,5})?\/(?:[^\s\/]+\/)*(?:[^\s]+\.(?:jpe?g|gif|png))' \
            '(?:\?\w+=\w+(?:&\w+=\w+)*)?)'

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
