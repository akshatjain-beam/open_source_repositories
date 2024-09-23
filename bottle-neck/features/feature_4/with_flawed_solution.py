```
    page_nav_data = {'limit': limit, 'offset': offset}
    page_count = int(math.ceil(record_count / float(limit))) or 1
    pagination = dict(total_count=record_count, total_pages=page_count)
    if page_count > 1:
        if offset >= limit:
            page_nav_data['offset'] = offset - limit
            pagination['prev_page'] = base_uri + page_nav_tpl.format(**page_nav_data)
        if (offset + limit) < record_count:
            page_nav_data['offset'] = offset + limit
            pagination['next_page'] = base_uri + page_nav_tpl.format(**page_nav_data)
    return pagination
```