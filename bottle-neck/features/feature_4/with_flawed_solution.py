```
    pagination = OrderedDict([
        ('total_count', record_count),
        ('total_pages', math.ceil(record_count / float(limit))),
        ('next_page', None),
        ('prev_page', None)
    ])
    if record_count > (offset + limit):
        pagination['next_page'] = '{}{}'.format(base_uri, page_nav_tpl.format(limit, offset + limit))
    if offset >= limit:
        pagination['prev_page'] = '{}{}'.format(base_uri, page_nav_tpl.format(limit, offset - limit))
    return pagination
```