'''
Created on 15.12.2013

@author: lotek
'''

import sys
import warnings

from . import _ENTRIEABLE_MODELS
from django.utils.translation import ugettext as _


_entrieable_reverse_names = []
_entrieable_auto_children = []
_auto_children_funcs = {}


def entrieable_reverse_name(name, app_name=None):
    global _entrieable_reverse_names
    fullname  = "%s:%s" % (app_name, name) if app_name else name
    _entrieable_reverse_names.append(fullname)
    # if auto_children:
    #    _entrieable_auto_children.append(name)
    #    _auto_children_funcs[name] = auto_children
    _entrieable_reverse_names = sorted([_f for _f in _entrieable_reverse_names if _f])
    return name

def entrieable_auto_populated(name, callback):
    _entrieable_auto_children.append(name)
    _auto_children_funcs[name] = callback

def entrieable_models():
    return _ENTRIEABLE_MODELS
