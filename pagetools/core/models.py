from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _, get_language
from model_utils.models import StatusModel, TimeStampedModel
from model_utils.choices import Choices
from concurrency.fields import IntegerVersionField
from . import settings as ptsettings


class LangManager(models.Manager):
    '''Manager for models with a lang-field'''
    def __init__(self, *args, **kwargs):
        super(LangManager, self).__init__(*args, **kwargs)
        self.use_lang = bool(getattr(settings, 'LANGUAGES', False))

    def lfilter(self, lang=None, **kwargs):
        '''uses keyword-argument or system-language to add 'lang' to filter-
        arguments if settings.LANGUAGES compares to not null'''
        if self.use_lang:
            if not lang:
                lang = get_language() or ""
            kwargs.update(lang__in=(lang, lang.split('-')[0], None, ''))
        return self.filter(**kwargs)


class LangModel(models.Model):
    '''Model with 'lang'-field'''
    objects = models.Manager()
    # public = LangManager()
    lang = models.CharField(
        max_length=20,
        choices=settings.LANGUAGES,
        blank=True,
        verbose_name=_('language')
    )

    class Meta:
        abstract = True


class PublishableLangManager(LangManager):
    '''Manager that finds published content language  filtered'''
    def lfilter(self, **kwargs):
        user = kwargs.pop('user', None)
        if not user or not user.is_authenticated():
            kwargs['status'] = ptsettings.STATUS_PUBLISHED

        return LangManager.lfilter(self, **kwargs)


class PublishableLangModel(LangModel, StatusModel):
    '''Model with model_utils...StatusModel for status and a language-field'''

    _translated_choices = [(slug, _(name))
                           for(slug, name)
                           in ptsettings.STATUS_CHOICES]
    STATUS = Choices(*_translated_choices)
    public = PublishableLangManager()

    def _enabled(self):
        return self.status == ptsettings.STATUS_PUBLISHED
    _enabled.boolean = True
    enabled = property(_enabled)

    class Meta:
        abstract = True


class PagelikeModel(TimeStampedModel, PublishableLangModel):
    '''This may everything that inclines a detail_view'''
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255)
    version = IntegerVersionField()

    def get_absolute_url(self):
        return '/%s' % self.slug

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


