'''
Created on 05.01.2014

@author: lotek

'''
from django.db import models

from django.utils import timezone


class BaseSubscriberMixin(models.Model):

    is_activated = models.BooleanField(default=False)
    subscribtion_date = models.DateTimeField(default=timezone.now())
    failures = models.IntegerField(default=0)

    def __unicode__(self):
        return self.email

    class Meta:
        abstract = True
