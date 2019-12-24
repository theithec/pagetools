from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from pagetools.core.utils import get_adminedit_url


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


class AdminLinkMixin:
    def admin_link(self, instance, linktext=None):
        linktext = linktext or "Edit"
        return format_html(
            '<a href="{}">{}</a>',
            get_adminedit_url(instance),
            linktext
        )
    admin_link.short_description = _("Admin link")

class PagelikeAdmin(AdminLinkMixin, TinyMCEMixin):
    '''
    Prepopulate slug from title and add tinymce-media
    '''
    prepopulated_fields = {"slug": ("title",)}

