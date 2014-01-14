'''
Created on 15.12.2013

@author: lotek
'''
from django.conf import settings


AREAS = getattr(settings, 'PT_AREAS',
                ((u'sidebar', 'Sidebar',),)
)

TEMPLATETAG_WIDGETS = getattr(settings, 'PT_TEMPLATETAG_WIDGETS', {})
