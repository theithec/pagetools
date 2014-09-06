'''
Created on 15.12.2013

@author: lotek
'''
from django.conf import settings


def _(x):
    return x


AREAS = getattr(settings, 'PT_AREAS',
                (('sidebar', _('Sidebar'),),)
                )

TEMPLATETAG_WIDGETS = getattr(settings, 'PT_TEMPLATETAG_WIDGETS', {})
