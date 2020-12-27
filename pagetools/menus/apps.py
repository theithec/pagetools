# pylint: disable=import-outside-toplevel
from typing import Any, Callable, Dict, List

from django.apps import AppConfig
from django.db import models


class MenusConfig(AppConfig):
    name = "pagetools.menus"
    verbose_name = "Menu administration"
    entrieable_reverse_names: List[str] = []
    entrieable_auto_children: List[Any] = []
    entrieable_models: List[models.Model] = []
    auto_children_funcs: Dict[str, Callable] = {}

    def ready(self):
        from django.contrib import admin

        reg = admin.site._registry
        models = []
        for model, admincls in reg.items():
            if getattr(admincls.__class__, "is_menu_entrieable", False):
                models.append(model)

        self.__class__.entrieable_models += sorted(models, key=str)
