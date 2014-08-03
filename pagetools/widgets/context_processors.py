from .utils import get_areas_for_type, type_or_none


def base_page(request=None):
    d = {}
    d['areas'] = get_areas_for_type(type_or_none('base'), {})
    return d

