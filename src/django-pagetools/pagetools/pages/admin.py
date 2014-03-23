'''
Created on 14.12.2013

@author: lotek
'''
from django.conf import settings
from django.contrib import admin

from pagetools.admin import PageLikeAdmin
from pagetools.menus.admin import EntrieableAdmin
from pagetools.pages.models import Page


class DynFieldAdmin(admin.TabularInline):
    model = None
    sortable_field_name = "position"
    extra = 1

class PageAdmin(EntrieableAdmin, PageLikeAdmin):
    readonly_fields = ('status_changed',)
    list_display = ('title', 'lang', 'status')
    list_filter = ('lang', 'status')
    search_fields = ('title', 'content')
    save_as = True
    class Meta:
        model = Page

admin.site.register(Page, PageAdmin)
