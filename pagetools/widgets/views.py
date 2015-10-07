from django.views.generic.base import View
from django.utils.translation import get_language
from slugify import slugify
from django.template.context_processors import csrf
from pagetools.core.views import BasePagelikeView

from .models import PageType
from .utils import get_areas_for_type


class WidgetViewMixin(object):

    def get_context_data(self, **kwargs):
        kwargs = super(WidgetViewMixin, self).get_context_data(**kwargs)
        ptname = self.get_pagetype_name(**kwargs)
        pt = self.get_pagetype(ptname=ptname, **kwargs)
        if pt:
            pt_descr = pt.pagetypedescription_set.filter(
                lang=get_language()).first()
            if pt_descr:
                kwargs['pagetype_description'] = pt_descr.description
        if kwargs.get("request", None) is None:
            kwargs.update(csrf(self.request))
        kwargs['areas'] = get_areas_for_type(pt, kwargs)
        kwargs['pagetype_name'] = ptname
        return kwargs


class WidgetPagelikeView(WidgetViewMixin, BasePagelikeView):

    def get_pagetype_name(self, **kwargs):
        ptname = kwargs.get('pagetype_name', None)
        if ptname is None:
            ptname = getattr(self, 'pagetype_name', None)
        return ptname

    def get_pagetype(self, ptname=None, **kwargs):
        if ptname is None:
            ptname = self.get_pagetype_name(**kwargs)
        if ptname:
            pt = None
            try:
                pt = PageType.objects.get(name=ptname)
            except PageType.DoesNotExist:
                pass
            return pt

    # reduce queries
    def get_object(self):
        if not getattr(self, 'object', None):
            self.object = super(BasePagelikeView, self).get_object()
        return self.object



