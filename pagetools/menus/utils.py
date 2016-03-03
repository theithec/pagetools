'''
Created on 15.12.2013

@author: lotek
'''

import sys
import warnings

from .settings import ENTRIEABLE_MODELS
from django.utils.translation import ugettext as _


_entrieable_reverse_names = []
_entrieable_auto_children = []
_auto_children_funcs = {}


def entrieable_reverse_name(name, auto_children=False):
    global _entrieable_reverse_names
    _entrieable_reverse_names.append(name)
    if auto_children:
        _entrieable_auto_children.append(name)
        _auto_children_funcs[name] = auto_children
    _entrieable_reverse_names = sorted([_f for _f in _entrieable_reverse_names if _f])
    return name


def entrieable_url(url):
    try:
        name = url.name
    except ValueError:
        raise ValueError(_('Entrieable urls need a name'))
    entrieable_reverse_name(name)
    return url


def entrieable_view(url):
    warnings.warn(_("deprecated, wrong naming, use entrieable_url"),
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
