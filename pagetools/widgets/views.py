from pagetools.core.views import BasePagelikeView
from .utils import get_areas_for_type


class WidgetViewMixin(object):
    def get_context_data(self, **kwargs):
        kwargs = super(WidgetViewMixin, self).get_context_data(**kwargs)
        ptname = self.get_pagetype_name(**kwargs)
        pt = self.get_pagetype(ptname=ptname, **kwargs)
        kwargs['areas'] = get_areas_for_type(pt, kwargs)
        kwargs['pagetype_name'] = ptname
        return kwargs


class WidgetPagelikeView(WidgetViewMixin, BasePagelikeView):
    pass