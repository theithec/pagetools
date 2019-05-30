'''
Created on 14.12.2013

@author: Tim Heithecker
'''
import os

from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from grappelli.forms import GrappelliSortableHiddenMixin

from pagetools.core.admin import PagelikeAdmin
from pagetools.menus.admin import EntrieableAdmin
from pagetools.pages.models import Page  # , DynFormField, PageDynFormField

from pagetools.menus.utils import entrieable_auto_populated
from pagetools.menus.models import MenuEntry


class BasePageAdmin(EntrieableAdmin, PagelikeAdmin):
    readonly_fields = ('status_changed',)
    list_display = ('title', 'lang', 'slug', 'status')
    list_filter = ('lang', 'status')
    search_fields = ('title', 'content')
    save_as = True

    class Media:
        js = [os.path.join(
            settings.STATIC_URL, 'pagetools', 'js', 'formreceiver.js')]


class PageAdmin(BasePageAdmin):
    # inlines = (PageDynFieldAdmin,)

    fieldsets = (
        ('', {'fields': [
            'lang',
            'status',
            'title',
            'slug',
            'description',
            'content',
        ]}),
        (_('Included form'), {'fields': [
            'included_form',
            'email_receivers',
        ]}),
        (_('Protection'), {'fields': [
            'login_required',
        ]}),
        (_('Show in menus'), {'fields': [
            'menus',
        ]}),
        (_('Pagetype'), {'fields': [
            'pagetype',
        ]}),
    )

    class Meta:
        model = Page


admin.site.register(Page, PageAdmin)


def pages_auto_entries():
    return [
        MenuEntry(title=p.title, content_object=p) for p in Page.public.all()]


entrieable_auto_populated("All pages", pages_auto_entries)


'''
class DynFieldInlineFormset(forms.models.BaseInlineFormSet):

    def clean(self):
        for form in self.forms:
            cd = form.cleaned_data
            if cd:
                # construct the field as validation
                form.instance.to_field()


class DynFieldAdmin(GrappelliSortableHiddenMixin, admin.StackedInline):
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
'''
