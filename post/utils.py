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
