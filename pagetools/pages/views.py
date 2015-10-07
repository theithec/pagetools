
# Create your views here.
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import BaseFormView

from pagetools.widgets.views import WidgetPagelikeView
from .models import Page

from .settings import MAILFORM_RECEIVERS


class IncludedFormView(DetailView, BaseFormView):
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
        if form_class and kwargs.get('form', True) is not None:
            kwargs['form'] = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.email_receivers = getattr(
            self.object, 'email_receivers', MAILFORM_RECEIVERS)
        if form.is_valid():
            messages.success(request, _("Mail send"))
            kwargs['form'] = None
            return self.get(request, *args, **kwargs)
        else:
            messages.error(request, _("An error occured"))
            return self.form_invalid(form)

    # todo rename
    def get_extras(self):
        d = {}
        try:
            d['extras'] = self.object.dynformfields.all()
        except AttributeError:
            pass
        return d

    def get_form_kwargs2(self):
        kwargs = super(IncludedFormView, self).get_form_kwargs()
        # kwargs.update(self.get_extras())
        return kwargs


class AuthPageView(DetailView):

    def get_queryset(self, *args, **kwargs):

        user = self.request.user
        d = {}
        if not user.is_authenticated():
            d['login_required'] = False
        d['user'] = user
        qs = self.model.public.lfilter(**d)
        return qs


class PageView(WidgetPagelikeView, AuthPageView, IncludedFormView):
    model = Page

    def get_pagetype_name(self, **kwargs):
        return (self.object.pagetype.name
                if self.object.pagetype
                else WidgetPagelikeView.get_pagetype_name(self, **kwargs))

    def get_pagetype(self, **kwargs):
        return self.object.pagetype or WidgetPagelikeView.get_pagetype(self)

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
