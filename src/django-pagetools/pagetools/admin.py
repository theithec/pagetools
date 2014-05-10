'''
Created on 14.12.2013

@author: lotek
'''
from django.conf import settings
from django.contrib import admin

from .settings import ADMIN_SET_LANG_FILTER

class TinyMCEMixin(object):
    class Media:
        js = [
            '%sgrappelli/tinymce/jscripts/tiny_mce/tiny_mce.js' % 
                                                    settings.STATIC_URL,
            '%sgrappelli/tinymce_setup/tinymce_setup.js' % 
                                                    settings.STATIC_URL,
        ]
        css = {
             'all': ('%spagetools/admin/css/pt_admin.css' % settings.STATIC_URL,)
        }


class PageLikeAdmin(TinyMCEMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
 
    


