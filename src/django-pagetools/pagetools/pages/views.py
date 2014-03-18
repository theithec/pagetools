# Create your views here.
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import get_urlconf, get_resolver
from django.http.response import Http404
from django.views.generic.detail import DetailView

from pagetools.views import BasePageView

from .models import Page


class IncludedFormView(DetailView):
    '''
        expects 
        object.includable_foms = { 'name1': Form1,
         [...]
        }

    '''
    included_form = None


    def get_formclass(self):
        obj = self.get_object()
        fname = obj.included_form
        if fname:
            FCls = obj.includable_forms.get(fname)
            return FCls
    
    def post(self, request, *args, **kwargs):
        FCls = self.get_formclass()
        self.included_form = None
        if FCls:
            self.included_form = FCls(self.request.POST)
        if self.included_form:
            if not self.included_form.is_valid(request=request):
                kwargs['form'] = self.included_form
            else:
                kwargs['form'] = None
                self.included_form = None
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.included_form:
            kwargs['form'] = self.included_form
        else:
            FCls = self.get_formclass()
            if FCls:
                kwargs['form'] = FCls()

        return super(IncludedFormView, self).get_context_data(**kwargs)


class AuthPageView(DetailView):

    def get_queryset(self, *args, **kwargs):
        return super(AuthPageView, self).get_queryset(*args, **kwargs).filter()
        user = self.request.user
        # 'slug': self.kwargs['slug'],
        d = {}
        if not user.is_authenticated():
            d['login_required'] = False
        qs = self.model.public.lfilter(**d)
        return qs

        return super(AuthPageView, self).get_queryset(*args, **kwargs).filter(**d)


class PageView(IncludedFormView, AuthPageView, BasePageView, DetailView,):
    # queryset = Page.objects.all()
    model = Page

    def get_pagetype(self, **kwargs):
        return self.object.pagetype

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = self.object.title
        return super(PageView, self).get_context_data(**kwargs)

class IndexView(PageView):
    #pagetype = 'index'

    def get_object(self, **kwargs):
        try:
            self.object = Page.public.get(
                slug='start',
            )
            return self.object
        except ObjectDoesNotExist:
            raise Http404

