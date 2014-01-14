'''
Created on 15.12.2013

@author: lotek
'''

import sys

from django.utils.functional import lazy

from .settings import ENTRIEABLE_MODELS


_entrieable_reverse_names = []


def entrieable_reverse_names(name):
    global _entrieable_reverse_names
    _entrieable_reverse_names.append(name)
    _entrieable_reverse_names = sorted(filter(None, _entrieable_reverse_names))
    


def entrieable_views(url):
    entrieable_reverse_names(url.name)
    return url


def entrieable_models():
    models = []
    for module, cls in ENTRIEABLE_MODELS:
        models.append(
            getattr(
                getattr(sys.modules[module], 'models'), cls
            )
        )
    return models
