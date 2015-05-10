'''
Created on 14.12.2013

@author: lotek
'''
from django.contrib import admin
from pagetools.core.admin import PagelikeAdmin
from .models import News


admin.site.register(News, PagelikeAdmin)




