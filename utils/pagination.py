from mongoengine.queryset.visitor import Q


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


def query_filter(event):
    query_params = event.get('queryStringParameters', {})
    if query_params is not None:
        filters = Q()
        if 'category' in query_params:
            filters &= Q(category=query_params['category'])
        if 'type' in query_params:
            filters &= Q(type=query_params['type'])
        if 'size' in query_params:
            filters &= Q(size=query_params['size'])
        if 'color' in query_params:
            filters &= Q(color=query_params['color'])
        if 'vendor' in query_params:
            filters &= Q(vendor=query_params['vendor'])
        if 'price_min' in query_params:
            filters &= Q(price__gte=float(query_params['price_min']))
        if 'price_max' in query_params:
            filters &= Q(price__lte=float(query_params['price_max']))
        if 'name' in query_params:
            filters &= Q(name__icontains=query_params['name'])
        return filters
    return Q()
