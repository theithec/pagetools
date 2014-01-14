'''
Created on 15.12.2013

@author: lotek
'''
from django.conf import settings


PAGE_PREFIX = getattr(settings, 'PT_PAGE_PREFIX', 'page/')

CONTACTFORM_RECEIVERS = getattr(settings,
    'PT_CONTACTFORM_RECEIVERS',
    [a[1] for a in settings.ADMINS]
)

