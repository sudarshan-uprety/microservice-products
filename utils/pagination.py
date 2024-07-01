def pagination(event):
    query_params = event.get('queryStringParameters', {})
    limit = 10
    page = 1
    if query_params is not None:
        page = int(query_params.get('page', 1))
        if page <= 1:
            skip = 0
        else:
            skip = (page-1) * 10  # page size is 10 by default
    else:
        skip = 0
    return limit, skip, page
