
'''
Created on 29.05.2013

@author: lotek
'''
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from grappelli.forms import GrappelliSortableHiddenMixin
from filebrowser.settings import ADMIN_THUMBNAIL

from pagetools.core.admin import PagelikeAdmin
from .models import PicPos, GalleryPic, Gallery


Basegalleryadmin = admin.ModelAdmin
if 'pagetools.menus' in settings.INSTALLED_APPS:
    from pagetools.menus.admin import EntrieableAdmin
    Basegalleryadmin = EntrieableAdmin



class BasePicPosAdmin(GrappelliSortableHiddenMixin, admin.TabularInline):
    fields = ( "pic",  "admin_link", "thumb", "position", )
    sortable_field_name = "position"
    readonly_fields = ( 'admin_link', 'thumb')
    extra = 2  # how many rows to show
    def admin_link(self, instance):
        realobj = instance.pic  # .content.get_real_obj()
        url = reverse('admin:%s_%s_change' % (realobj._meta.app_label,
                                              realobj._meta.model_name),
                      args=(realobj.id,))
        return format_html(u'<a href="{}">edit</a>', url)
    admin_link.allow_tags = True
    admin_link.short_description = _("Title and Path")
    def thumb(self, instance):
        t =  '<img src="%s" />' % instance.pic.pic.version_generate(ADMIN_THUMBNAIL).url
        return t
    thumb.allow_tags = True
    thumb.short_description = _("Thumbnail")



class PicPosAdmin(admin.TabularInline):
    model = PicPos


class GalleryAdmin(Basegalleryadmin):
    inlines = (PicPosAdmin,)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register((GalleryPic, PicPos,))
admin.site.register(Gallery, GalleryAdmin)
