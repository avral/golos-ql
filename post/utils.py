import re
import html


PROXIFY_REGEX = (r'((?!https:\/\/imgp.golos)https?:\/\/(?:[\da-zA-Z]{1}'
                 '(?:[\w\-\.]+\.)+(?:[\w]{2,5}))(?:\:[\d]{1,5})?\/(?:[^\s\/]+'
                 '\/).*?\.(?:jpe?g|gif|png)(?:\?\w+=\w+(?:\&\w+=\w+)*)?)')


LINKIFY_REGEX = (r'((?<![\"\(\/])https?:\/\/(?:[\da-zA-Z]{1}(?:[\w\-\.]+\.)+'
                 '(?:[\w]{2,5}))(?:\:[\d]{1,5})?\/(?:[^\s\/]+\/).*?\.'
                 '(?:jpe?g|gif|png)(?:\?\w+=\w+(?:\&\w+=\w+)*)?)')


IMAGE_TEMPLATE = {
    'html': r'<img src="\1"></img>',
    'markdown': r'![](\1)',
    None: '\1'
}


def qs_ab_filter(qs, args):
    after = args.pop('after', False)
    before = args.pop('before', False)

    if after:
        cursor = qs.get(id=after)
        qs = qs.filter(__raw__={
            '_id': {'$ne': cursor.id},
            'created': {'$lte': cursor.created}
        })
    if before:
        cursor = qs.get(id=before)
        qs = qs.filter(__raw__={
            '_id': {'$ne': cursor.id},
            'created': {'$gte': cursor.created}
        })

    return qs


def linkify_images(body, format=None):
    if format == 'html':
        body = html.unescape(body)

    # Proxyfi all images
    body = re.sub(PROXIFY_REGEX, r'https://imgp.golos.io/0x0/\1', body)

    return re.sub(LINKIFY_REGEX, IMAGE_TEMPLATE[format], body)
