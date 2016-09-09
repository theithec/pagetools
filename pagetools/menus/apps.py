from django.apps import AppConfig


class MenusConfig(AppConfig):
    name = "pagetools.menus"
    verbose_name = "Menu administration"

    def ready(self):
        from django.contrib import admin
        from . import _ENTRIEABLE_MODELS
        reg = admin.site._registry
        models = []
        for model, admincls in reg.items():
            if getattr(admincls.__class__, 'is_menu_entrieable', False):
                models.append(model)

        _ENTRIEABLE_MODELS += sorted(models, key=str)
