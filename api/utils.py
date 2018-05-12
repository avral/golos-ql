from models import Comment


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
