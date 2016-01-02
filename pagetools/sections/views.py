from django.views.generic import DetailView, FormView
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, FormView, TemplateView
from django.utils.html import format_html
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django_ajax.decorators import ajax
from django_ajax.mixin import AJAXMixin
from .utils import get_template_names_for_obj
from .models import PageNode
from .dashboard_modules import PageNodesModule


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
        #  context['scale'] = "0.9"
        return context

class BaseAjaxNodeView(BaseAjaxNodeViewMixin, BaseNodeView):
    pass


def _add_children(txt, children, user):
    for c in children:
        adminediturl = reverse(
            'admin:%s_%s_change' % (
                c._meta.app_label,
                c._meta.model_name
            ),
            args=(c.id,))

        txt += format_html(
            '''<li><a {} href="{}">{}</a>''',
            "" if c.enabled else mark_safe("style='color: orange;'"),
            adminediturl,
            c
        )
        coc = c.ordered_content(user=user)
        if coc:
            txt += '<ul>' + _add_children('', coc, user) + '</ul>'
        txt += "</li>"
    return txt

@ajax
@login_required
def admin_pagenodesview(request, slug):
    p = PageNodesModule.model.objects.get(slug=slug)
    listtxt = '<ol id="pagenodes">'
    listtxt += _add_children('',
                             [p],
                             user=request.user)
    listtxt += '</ol>'
    return HttpResponse(listtxt)


