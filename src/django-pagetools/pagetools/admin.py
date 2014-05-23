'''
Created on 14.12.2013

@author: lotek
'''
from django.conf import settings
from django.contrib import admin

from .settings import ADMIN_SET_LANG_FILTER


def fieldset_copy(fieldset):
    fscopy = (fieldset[0],
              {'fields': [f for f in fieldset[1]['fields']]}
             )
    clzs = fieldset[1].get('classes')
    if clzs:
        fscopy[1]['classes'] = [c for c in clzs]
    return fscopy

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
 
    


