# pylint: disable=import-outside-toplevel
from django.apps import AppConfig


class MenusConfig(AppConfig):
    name = "pagetools.menus"
    verbose_name = "Menu administration"
    entrieable_reverse_names = []
    entrieable_auto_children = []
    entrieable_models = []
    auto_children_funcs = {}

    def ready(self):
        from django.contrib import admin
        reg = admin.site._registry
        models = []
        for model, admincls in reg.items():
            if getattr(admincls.__class__, 'is_menu_entrieable', False):
                models.append(model)

        self.__class__.entrieable_models += sorted(models, key=str)
