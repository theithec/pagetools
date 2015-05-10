'''
Created on 29.05.2013

@author: lotek
'''
from django.contrib import admin
from .models import PicPos, GalleryPic, Gallery
from pagetools.core.admin import PagelikeAdmin
from pagetools.menus.admin import EntrieableAdmin


class PicPosAdmin(admin.TabularInline):
    model = PicPos
    fields = ("pic", "position")
    sortable_field_name = "position"
    extra = 2  # how many rows to show


class GalleryAdmin(PagelikeAdmin, EntrieableAdmin):
    inlines = (PicPosAdmin,)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register((GalleryPic, PicPos,))
admin.site.register(Gallery, GalleryAdmin)
