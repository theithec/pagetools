'''
all copy&paste from
https://github.com/fcurella/django/commit/de11e7b795defb91a0db0e3ddbad746ed4bfbd56
'''
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
import re
slug_unicode_re = re.compile(r'^[-\w_]+$', re.U)
validate_unicode_slug = RegexValidator(
    slug_unicode_re,
    _("Enter a valid 'slug' consisting of unicode letters, numbers, underscores or hyphens."),
    'invalid')
