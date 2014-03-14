'''
Created on 14.12.2013

@author: lotek
'''
from django.conf import settings
from django.contrib import admin

from pagetools.admin import PageLikeAdmin
from pagetools.menus.admin import EntrieableAdmin
from pagetools.pages.models import Page


class PageAdmin(EntrieableAdmin, PageLikeAdmin):
    readonly_fields = ('status_changed',)
    list_display = ('title', 'lang', 'status')
    # -> unicode error @ 1&1 
    # filter_horizontal = ('topics',)
    list_filter = ('lang', 'status')
    search_fields = ('title', 'content')
    save_as = True
    class Meta:
        model = Page

admin.site.register(Page, PageAdmin)
