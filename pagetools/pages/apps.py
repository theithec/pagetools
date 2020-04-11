# pylint: disable=import-outside-toplevel
from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = "pagetools.pages"
    includable_forms = {}

    def ready(self):
        from . import forms
        self.includable_forms = {
            'Contactform': forms.ContactForm,
            'Contactfrom(Captcha)': forms.CaptchaContactForm,
        }
