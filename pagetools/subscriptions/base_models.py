'''
Created on 05.01.2014

@author: Tim Heithecker

'''
from django.db import models

from django.utils import timezone


class BaseSubscriberMixin(models.Model):

    is_activated = models.BooleanField(default=False)
    subscribtion_date = models.DateTimeField(auto_now_add=True)
    failures = models.IntegerField(default=0)

    def __str__(self):
        return self.get_email()

    def cmd_path(self):
        return ""

    @classmethod
    def get_subscribers(cls, **kwargs):
        return cls.objects.filter(is_activated=True)

    class Meta:
        abstract = True
