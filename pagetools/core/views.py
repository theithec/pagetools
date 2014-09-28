'''
Created on 20.12.2013

@author: lotek
'''
from django.conf import settings
from django.template.defaultfilters import slugify
from django.views.generic import View
from django.views.generic.list import ListView


class BasePagelikeView(View):

    def get_context_data(self, *args, **kwargs):
        kwargs = super(BasePagelikeView, self).get_context_data(**kwargs)
        sel = kwargs.get('selected', [])
        sel.append(self.get_slug())
        kwargs['selected'] = sel
        return kwargs

    def get_slug(self):
        try:
            return self.get_object().slug
        except AttributeError:
            try:
                return super(BasePagelikeView, self).get_slug()
            except AttributeError:
                return slugify(self.__class__.__name__)

    # reduce queries
    def get_object(self):
        if not getattr(self, 'object', None):
            self.object = super(BasePagelikeView, self).get_object()
        return self.object

class PubLangFilteredView(View):
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        # call lazy obj
        user.is_authenticated()
        return self.model.public.lfilter(user=user)

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
