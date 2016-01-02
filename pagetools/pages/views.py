
# Create your views here.
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin

from pagetools.widgets.views import WidgetPagelikeMixin
from pagetools.menus.views import SelectedMenuentriesMixin
from .models import Page

from .settings import MAILFORM_RECEIVERS


class IncludedFormMixin(object):
    '''
        expects in object
        includable_forms = { 'name1': Form1,
         [...]
        }

    '''
    included_form = None
    success_url = "/"

    def get_form_class(self):
        self.object = self.get_object()
        fname = self.object.included_form
        if fname:
            FCls = self.object.includable_forms.get(fname)
            return FCls

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        if form_class and kwargs.get('form', None) is None:
            FC = self.get_form_class()
            fkwargs = self.get_form_kwargs()
            kwargs['form'] = FC(**fkwargs)
        return self.render_to_response(self.get_context_data(**kwargs))


    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            kwargs['form'] = None
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'data':_("Mail send")}, status=200)
        else:
            messages.success(self.request, _("Mail send"))
            return self.get(self.request, form=None)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            messages.error(self.request, _("An error occured"))
        return self.get(self.request, form=form)

    '''
    # todo rename
    def get_extras(self):
        d = {}
        try:
            d['extras'] = self.object.dynformfields.all()
        except AttributeError:
            pass
        return d
    '''

    def get_form_kwargs(self):
        kwargs = {}
        if getattr(self, 'object') and getattr(self.object, 'email_receivers'):
            kwargs['email_receivers'] = self.object.email_receivers
        # kwargs.update(self.get_extras())
        return kwargs


class AuthPageMixin(object):

    def get_queryset(self, *args, **kwargs):

        user = self.request.user
        d = {}
        if not user.is_authenticated():
            d['login_required'] = False
        d['user'] = user
        qs = self.model.public.lfilter(**d)
        return qs


class PageView(
        SelectedMenuentriesMixin,
        WidgetPagelikeMixin,
        AuthPageMixin,
        IncludedFormMixin,
        DetailView):

    model = Page

    def get_pagetype_name(self, **kwargs):
        return (
            self.object.pagetype.name
            if self.object.pagetype
            else super().get_pagetype_name(**kwargs))

    def get_pagetype(self, **kwargs):
        return self.object.pagetype or super().get_pagetype(self)

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = self.object.title
        # obj = self.get_object()
        kwargs = super(PageView, self).get_context_data(**kwargs)
        return kwargs


class IndexView(PageView):

    def get_object(self, **kwargs):
        try:
            self.object = self.get_queryset().get(
                slug="start"
            )
            return self.object
        except ObjectDoesNotExist:
            raise Http404
