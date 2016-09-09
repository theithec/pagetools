'''
Created on 26.02.2012

@author: Tim Heithecker
'''
from django.contrib import admin

from .models import QueuedEmail, SendStatus, Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_activated')


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(QueuedEmail)
admin.site.register(SendStatus)
