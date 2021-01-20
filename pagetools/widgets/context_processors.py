from .utils import get_areas_for_type, type_or_none


def base_pagetype(request=None):
    d = {}
    d["areas"] = get_areas_for_type(type_or_none("base"), {})
    return d


def pagetype_from_view(request):
    func = request.resolver_match.func
    obj = getattr(func, "view_class", None)
    context = {}
    if not getattr(obj, "add_pagetype_promise", False) and not getattr(request, "areas_added", False):
        pagetype_name = getattr(obj, "pagetype_name", "base")
        context = {"areas": get_areas_for_type(type_or_none(pagetype_name), context, request)}
    return context
