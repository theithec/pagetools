'''Core models for pagetools
'''

import warnings
import django
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _, get_language

from model_utils.models import StatusModel, TimeStampedModel
from model_utils.choices import Choices

from . import settings as ptsettings


class LangManager(models.Manager):
    '''
    Manager for models with a lang-field
    '''
    def __init__(self, *args, **kwargs):
        super(LangManager, self).__init__(*args, **kwargs)
        self.use_lang = bool(getattr(settings, 'LANGUAGES', False))

    def lfilter(self, lang=False, **kwargs):
        '''Uses keyword-argument or system-language to add 'lang' to filter-
        arguments if settings.LANGUAGES compares not to null'''

        if self.use_lang and not kwargs.pop('skip_lang', False):
            if lang is False:
                lang = get_language() or ""
            kwargs.update(lang__in=(lang, lang.split('-')[0], ''))
        return self.filter(**kwargs)


class LangModel(models.Model):
    '''
    Model with ``lang``-field.

    Note:
        To avoid `NOT NULL constraint failed` errors,
        empty lang is saved as "".
    '''
    objects = models.Manager()
    # public = LangManager()
    lang = models.CharField(
        max_length=20,
        choices=settings.LANGUAGES,
        blank=True,
        verbose_name=_('language')
    )

    def save(self, *args, **kwargs):
        if self.lang is None:
            self.lang = ''
        super(LangModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class PublishableLangManager(LangManager):
    '''
    Manager that finds published content language filtered
    '''

    def lfilter(self, **kwargs):
        '''
        For non authenticated users returns only published content
        and filters for language (if settings.LANGUAGES has entries)
        See :class: `LangManager`
        '''

        user = kwargs.pop('user', None)
        if not user or not user.is_authenticated():
            kwargs['status'] = ptsettings.STATUS_PUBLISHED
        return LangManager.lfilter(self, **kwargs)


class PublishableLangModel(LangModel, StatusModel):
    '''
    Model with a language and a status field and a ``PublishableLangManager``
    '''

    _translated_choices = [(slug, _(name))
                           for(slug, name)
                           in ptsettings.STATUS_CHOICES]
    STATUS = Choices(*_translated_choices)
    public = PublishableLangManager()

    def _enabled(self):
        warnings.warn("Depricated. Bad naming. Use ``is_published``.")
        return self.status == ptsettings.STATUS_PUBLISHED
    _enabled.boolean = True
    _enabled.admin_order_field = 'status'
    enabled = property(_enabled)

    def _is_published(self):
        return self.status == ptsettings.STATUS_PUBLISHED
    _is_published.boolean = True
    _is_published.admin_order_field = 'status'
    is_published = property(_is_published)

    class Meta:
        abstract = True


#  c&p from django1.9
from django.core.validators import RegexValidator
import re
import six
from django.utils.functional import SimpleLazyObject


def _lazy_re_compile(regex, flags=0):
    """Lazily compile a regex with flags."""
    def _compile():
        # Compile the regex if it was not passed pre-compiled.
        if isinstance(regex, six.string_types):
            return re.compile(regex, flags)
        else:
            assert not flags, "flags must be empty if regex is passed pre-compiled"
            return regex
    return SimpleLazyObject(_compile)
slug_unicode_re = _lazy_re_compile(r'^[-\w]+\Z', re.U)
validate_unicode_slug = RegexValidator(
    slug_unicode_re,
    _("Enter a valid 'slug' consisting of Unicode letters, numbers, underscores, or hyphens."),
    'invalid'
)
class _USlugField(models.CharField):
    '''Slugfield that allows unicode'''
    default_validators = [validate_unicode_slug]
USlugField = _USlugField


class PagelikeModel(TimeStampedModel, PublishableLangModel):
    '''
    This could be a base model for everything that inclines a detail_view

    Args:
        title (str)
        slug (str)
        description (Optional[str]): for metatag/seo
    '''

    title = models.CharField(_('Title'), max_length=255)
    slug = None
    if django.VERSION<(1, 9):
        slug = USlugField(_('Slug'), max_length=255)
    else:
        slug = models.SlugField(_('Slug'), max_length=255, allow_unicode=True)
    description = models.CharField(
        _('Description'),
        max_length=139,
        help_text='''Description (for searchengines)''', blank=True)


    def get_absolute_url(self):
        return '/%s' % self.slug

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
