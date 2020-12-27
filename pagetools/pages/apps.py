# pylint: disable=import-outside-toplevel
from typing import Dict
from django.forms import Form
from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = "pagetools.pages"
    includable_forms: Dict[str, Form] = {}

    def ready(self):
        from . import forms

        self.includable_forms = {
            "Contactform": forms.ContactForm,
            "Contactfrom(Captcha)": forms.CaptchaContactForm,
        }
