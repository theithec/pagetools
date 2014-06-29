'''
Created on 15.12.2013

@author: lotek
'''

import sys
import warnings

from .settings import ENTRIEABLE_MODELS


_entrieable_reverse_names = []


def entrieable_reverse_name(name):
    global _entrieable_reverse_names
    _entrieable_reverse_names.append(name)
    _entrieable_reverse_names = sorted(filter(None, _entrieable_reverse_names))
    return name


def entrieable_url(url):
    try:
        name = url.name
    except ValueError:
        raise ValueError('Entrieable urls need a name')
    entrieable_reverse_name(name)
    return url


def entrieable_view(url):
    warnings.warn("deprecated, wrong naming, use entrieable_url",
                  DeprecationWarning)
    return entrieable_url(url)


def entrieable_models():
    models = []
    for module, cls in ENTRIEABLE_MODELS:
        models.append(
            getattr(
                getattr(sys.modules[module], 'models'), cls
            )
        )
    return models
