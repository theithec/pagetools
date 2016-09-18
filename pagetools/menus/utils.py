'''
Created on 15.12.2013

@author: Tim Heithecker
'''

from . import _ENTRIEABLE_MODELS

_entrieable_reverse_names = []
_entrieable_auto_children = []
_auto_children_funcs = {}


def entrieable_reverse_name(name, app_name=None):
    global _entrieable_reverse_names
    fullname  = "%s:%s" % (app_name, name) if app_name else name
    _entrieable_reverse_names.append(fullname)
    _entrieable_reverse_names = sorted([_f for _f in _entrieable_reverse_names if _f])
    return name

# todo prefix add_
def entrieable_auto_populated(name, callback):
    _entrieable_auto_children.append(name)
    _auto_children_funcs[name] = callback

def entrieable_models():
    models = []
    for model in _ENTRIEABLE_MODELS:
        validator =  getattr(model, 'show_in_menu_add', None)
        if not validator or validator():
            models.append(model)
    return models
