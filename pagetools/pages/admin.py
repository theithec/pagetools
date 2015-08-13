'''
Created on 14.12.2013

@author: lotek
'''
import os

from django import forms
from django.conf import settings
from django.contrib import admin

#from concurrency.admin import ConcurrentModelAdmin
from pagetools.core.admin import PagelikeAdmin
from pagetools.menus.admin import EntrieableAdmin
from pagetools.pages.models import Page, DynFormField, PageDynFormField


class DynFieldInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            cd = form.cleaned_data
            if cd:
                # construct the field as validation
                form.instance.to_field()


class DynFieldAdmin(admin.StackedInline):
    model = DynFormField
    sortable_field_name = "position"
    extra = 1
    formset = DynFieldInlineFormset

    class Media:
        js = [os.path.join(
            settings.STATIC_URL, 'pagetools', 'js', 'dynfield.js')]


class PageDynFieldAdmin(DynFieldAdmin):
    model = PageDynFormField
    sortable_field_name = "position"
    extra = 1
    formset = DynFieldInlineFormset


class PageAdmin(EntrieableAdmin, PagelikeAdmin):
    inlines = (PageDynFieldAdmin,)
    readonly_fields = ('status_changed',)
    list_display = ('title', 'lang', 'status')
    list_filter = ('lang', 'status')
    search_fields = ('title', 'content')
    save_as = True

    class Meta:
        model = Page

admin.site.register(Page, PageAdmin)
