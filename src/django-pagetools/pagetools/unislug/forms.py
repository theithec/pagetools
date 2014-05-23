'''
all copy&paste from
https://github.com/fcurella/django/commit/de11e7b795defb91a0db0e3ddbad746ed4bfbd56
'''
from django.forms.fields import SlugField
from . import validators


class UnicodeSlugField(SlugField):
    default_validators = [validators.validate_unicode_slug]
    
