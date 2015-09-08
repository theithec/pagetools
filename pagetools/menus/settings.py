'''
Created on 15.12.2013

@author: lotek
'''
from django.conf import settings


ENTRIEABLE_MODELS = getattr(
    settings,
    'PT_ENTRIEABLE_MODELS',
    (
        ('pagetools.pages', 'Page'),
        ('pagetools.menus', 'Link'),
        ('pagetools.menus', 'ViewLink'),
    )
)

MENU_TEMPLATE = getattr(
    settings,
    'PT_MENU_TEMPLATE',
    'pagetools/menus/menu.html'
)
