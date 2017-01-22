'''
Created on 14.12.2013

@author: Tim Heithecker
'''

from django.conf import settings
from django.contrib import admin


def fieldset_copy(fieldset):
    '''ugly helper for reuse of filedsets'''
    fscopy = (
        fieldset[0],
        {'fields': [f for f in fieldset[1]['fields']]}
    )
    clzs = fieldset[1].get('classes', None)
    if clzs:
        fscopy[1]['classes'] = [c for c in clzs]

    return fscopy


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
