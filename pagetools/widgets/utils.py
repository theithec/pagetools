'''
Created on 22.05.2013

@author: lotek
'''

from pagetools.widgets.models import PageType, TypeArea
# from _mysql_exceptions import Error
from django.db.utils import DatabaseError
from django.utils.text import slugify


def type_or_none(typename):
    try:
        return PageType.objects.get(name=typename)
    except(PageType.DoesNotExist, DatabaseError):
        return None


def get_areas_for_type(pagetype, contextdict, tmpdict=None):
    if not tmpdict:
        tmpdict = {}

    if pagetype is None:
        pagetype = type_or_none('base')
        if not pagetype:
            return
        return get_areas_for_type(pagetype, contextdict, tmpdict)
    tas = TypeArea.objects.lfilter(type=pagetype)
    for ta in tas:
        if tmpdict.get(ta.area) is not None:
            continue
        orderedwidgets = ta.widgets.filter(enabled=True).order_by('position')
        tmpdict[ta.area] = [
            {'title': w.get_title(),
             'content': w.get_content(contextdict),
             'type': slugify('%s' % w.content_type)
             }
            for w in orderedwidgets  # allareawidgets
        ]
        # print "tmpdict", tmpdict
    if pagetype.parent:
        tmpdict = get_areas_for_type(
            pagetype.parent,
            contextdict,
            tmpdict
        )
    return tmpdict
