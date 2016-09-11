'''
Created on 15.12.2013

@author: lotek
'''
from django.conf import settings

MENU_TEMPLATE = getattr(
    settings,
    'PT_MENU_TEMPLATE',
    'menu.html'
)
