'''
Created on 14.12.2013

@author: Tim Heithecker
'''
from django.conf import settings
from django.contrib import admin


class TinyMCEMixin(admin.ModelAdmin):
    '''
    Add tinymce media files
    '''

    class Media:

        js = [
            '%sgrappelli/tinymce/jscripts/tiny_mce/tiny_mce.js' %
            settings.STATIC_URL,
            '%sgrappelli/tinymce_setup/tinymce_setup.js' %
            settings.STATIC_URL,
        ]
        '''Sphinx shows this as a hardcoded string, but it is not.'''


class PagelikeAdmin(TinyMCEMixin):
    '''
    Prepopulate slug from title and add tinymce-media
    '''
    prepopulated_fields = {"slug": ("title",)}
