'''
Created on 29.05.2013

@author: lotek
'''
from django.contrib import admin
from django.conf import settings
from .models import PicPos, GalleryPic, Gallery
from pagetools.core.admin import PagelikeAdmin


Basegalleryadmin = admin.ModelAdmin
if 'pagetools.menus' in settings.INSTALLED_APPS:
    from pagetools.menus.admin import EntrieableAdmin
    Basegalleryadmin = EntrieableAdmin



class PicPosAdmin(admin.TabularInline):
    model = PicPos
    fields = ("pic", "position")
    sortable_field_name = "position"
    extra = 2  # how many rows to show


class GalleryAdmin(Basegalleryadmin):
    inlines = (PicPosAdmin,)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register((GalleryPic, PicPos,))
admin.site.register(Gallery, GalleryAdmin)
