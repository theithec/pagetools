'''
Created on 20.12.2013

@author: lotek
'''
from django.conf import settings
from django.template.defaultfilters import slugify
from django.views.generic import View
from django.views.generic.list import ListView
from pagetools.widgets.models import PageType
from pagetools.widgets.utils import get_areas_for_type



class BasePageView(View):

    def get_context_data(self, *args, **kwargs):
        kwargs = super(BasePageView, self).get_context_data(*args, **kwargs)
        sel = kwargs.get('selected', [])
        sel.append(self.get_slug())
        kwargs['selected'] = sel 
        
        if 'pagetools.widgets' in settings.INSTALLED_APPS:
            pt = self.get_pagetype(**kwargs)
            kwargs['areas'] = get_areas_for_type(pt, kwargs)
        return kwargs
    
    def get_pagetype(self, **kwargs):
        pt = None
        ptname = kwargs.get('pagetype_name', None)
        if ptname == None:
            ptname = getattr(self, 'pagetype_name', None)
        if ptname:
            try:
                pt = PageType.objects.get(name=ptname)
            except PageType.DoesNotExist:
                pass
        return pt
    
    
    def get_slug(self):
        try:
            return self.get_object().slug
        except AttributeError:
            n = slugify(self.__class__.__name__)
            return n

    
class PaginatorMixin(ListView):
    paginate_by = getattr(settings, 'PAGINATE_BY', 20)
    sep = '?'

    def get_context_data(self, **kwargs):
        context = super(PaginatorMixin, self).get_context_data(**kwargs)
        page = context['page_obj']
        paginator = page.paginator
        _from = page.number - 5 if page.number > 5 else 0
        context['curr_page_range'] = paginator.page_range[_from:page.number + 5]
        context['get_sep'] = self.sep
        
        return context

