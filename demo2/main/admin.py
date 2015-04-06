from django.contrib import admin
from pagetools.core.admin import PagelikeAdmin
from .models import BlogEntry

admin.site.register(BlogEntry, PagelikeAdmin)
