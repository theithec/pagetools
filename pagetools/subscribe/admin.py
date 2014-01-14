'''
Created on 26.02.2012

@author: lotek
'''
from django.contrib import admin

from .models import QueuedEmail, SendStatus, Subscriber

admin.site.register(Subscriber)
admin.site.register(QueuedEmail)
admin.site.register(SendStatus)

