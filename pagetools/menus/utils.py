from . import _ENTRIEABLE_MODELS
from .apps import MenusConfig


def entrieable_reverse_name(name, app_name=None):
    fullname = "%s:%s" % (app_name, name) if app_name else name
    MenusConfig.entrieable_reverse_names.append(fullname)
    MenusConfig.entrieable_reverse_names = sorted([_f for _f in MenusConfig.entrieable_reverse_names if _f])
    return name


def entrieable_auto_populated(name, callback):
    MenusConfig.entrieable_auto_children.append(name)
    MenusConfig.auto_children_funcs[name] = callback


def entrieable_models():
    models = []
    for model in _ENTRIEABLE_MODELS:
        validator = getattr(model, 'show_in_menu_add', None)
        if not validator or validator():
            models.append(model)
    return models
