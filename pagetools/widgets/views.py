from django.utils.translation import get_language
from django.template.context_processors import csrf

from .models import PageType
from .utils import get_areas_for_type


class WidgetViewMixin:

    add_pagetype_promise = True
    '''If set, the widget context processor will not adding areas'''

    def get_context_data(self, **kwargs):
        kwargs = super(WidgetViewMixin, self).get_context_data(**kwargs)
        ptname = self.get_pagetype_name(**kwargs)
        ptype = self.get_pagetype(ptname=ptname, **kwargs)
        if ptype:
            pt_descr = ptype.pagetypedescription_set.filter(
                lang=get_language()).first()
            if pt_descr:
                kwargs['pagetype_description'] = pt_descr.description
        if kwargs.get("request", None) is None:
            kwargs.update(csrf(self.request))
        kwargs['areas'] = get_areas_for_type(ptype, kwargs)
        kwargs['pagetype_name'] = ptname
        return kwargs


class WidgetPagelikeMixin(WidgetViewMixin):

    def get_pagetype_name(self, **kwargs):
        ptname = kwargs.get('pagetype_name', None)
        if ptname is None:
            ptname = getattr(self, 'pagetype_name', None)
        return ptname

    def get_pagetype(self, ptname=None, **kwargs):
        ptype = None
        if ptname is None:
            ptname = self.get_pagetype_name(**kwargs)
        if ptname:
            try:
                ptype = PageType.objects.get(name=ptname)
            except PageType.DoesNotExist:
                pass

        return ptype
