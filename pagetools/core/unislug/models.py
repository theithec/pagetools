'''
all copy&paste from
https://github.com/fcurella/django/commit/de11e7b795defb91a0db0e3ddbad746ed4bfbd56
'''
from django.db.models.fields import SlugField
from . import validators, forms


class UnicodeSlugField(SlugField):

    default_validators = [validators.validate_unicode_slug]

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.UnicodeSlugField}
        defaults.update(kwargs)
        return super(UnicodeSlugField, self).formfield(**defaults)
