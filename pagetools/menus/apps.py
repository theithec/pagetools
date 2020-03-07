# pylint: disable=import-outside-toplevel
from django.apps import AppConfig


class MenusConfig(AppConfig):
    name = "pagetools.menus"
    verbose_name = "Menu administration"
    entrieable_reverse_names = []
    entrieable_auto_children = []
    auto_children_funcs = {}

    def ready(self):
        from django.contrib import admin
        from . import _ENTRIEABLE_MODELS
        reg = admin.site._registry
        models = []
        for model, admincls in reg.items():
            if getattr(admincls.__class__, 'is_menu_entrieable', False):
                models.append(model)

        _ENTRIEABLE_MODELS += sorted(models, key=str)
