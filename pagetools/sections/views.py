from django.views.generic import DetailView, FormView
from django.http import HttpResponseRedirect
from django_ajax.mixin import AJAXMixin
from .utils import get_template_names_for_obj
from .models import PageNode


class BaseNodeView(DetailView):
    model = PageNode

    def get_queryset(self, *args, **kwargs):
        return self.model.public.lfilter(user=self.request.user)

    def get_object(self, *args, **kwargs):
        o = super(BaseNodeView, self).get_object(*args, **kwargs)
        return o.get_real_obj()

    def get_template_names(self):
        return self.template_name or get_template_names_for_obj(self.object) or \
            super(BaseNodeView, self).get_template_names()

    def get_context_data(self, **kwargs):
        context = super(BaseNodeView, self).get_context_data(**kwargs)
        #if self.object.positioned_content:
        context['contents'] = self.object.ordered_content(
                user=self.request.user)
        return context

class BaseAjaxNodeViewMixin(AJAXMixin):
    def get_context_data(self, **kwargs):
        context = super(BaseAjaxNodeViewMixin, self).get_context_data(**kwargs)
        context['AJAXVIEW'] = True
        context['css_block'] = "css_ajax"
        context['js_block'] = "css_ajax"
        context['scale'] = "0.9"
        return context

class BaseAjaxNodeView(BaseAjaxNodeViewMixin, BaseNodeView):
    pass
