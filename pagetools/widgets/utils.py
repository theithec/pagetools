from django.db.utils import DatabaseError

from pagetools.widgets.models import PageType, TypeArea


def type_or_none(typename):
    try:
        return PageType.objects.get(name=typename)
    except (PageType.DoesNotExist, DatabaseError):
        return None


def get_areas_for_type(pagetype, contextdict, request, tmpdict=None):
    request.areas_added = True
    if not tmpdict:
        tmpdict = {}

    if pagetype is None:
        pagetype = type_or_none("base")
        if not pagetype:
            return None

        return get_areas_for_type(pagetype, contextdict, request, tmpdict)
    type_areas = TypeArea.objects.lfilter(pagetype=pagetype)
    for type_area in type_areas:
        if tmpdict.get(type_area.area) is not None:
            continue

        orderedwidgets = (
            type_area.widgets.filter(enabled=True)
            .prefetch_related("content_object")
            .order_by("position")
        )
        tmpdict[type_area.area] = [
            widget.get_content(contextdict, request) for widget in orderedwidgets
        ]

    if pagetype.parent:
        tmpdict = get_areas_for_type(pagetype.parent, contextdict, request, tmpdict)
    return tmpdict
