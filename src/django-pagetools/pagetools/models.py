from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _, get_language
from model_utils.choices import Choices
from model_utils.managers import QueryManager
from model_utils.models import StatusModel, TimeStampedModel

import settings as ptsettings
from unislug.models  import UnicodeSlugField


class LangManager(QueryManager):
    def __init__(self, *args, **kwargs):
        super(LangManager, self).__init__(*args, **kwargs)
        self.use_lang = bool(getattr(settings, 'LANGUAGES', False))

    def lfilter(self, lang=None, **kwargs):
        if self.use_lang:
            if not lang:
                lang = get_language()
                kwargs.update(lang__in=(lang, lang.split('-')[0], None, u''))
        return self.filter(**kwargs)
    


class LangModel(models.Model):
    public = LangManager()
    lang = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        blank=True,
        verbose_name=_('language')
    )

    class Meta:
        abstract = True


class PublishableModel(StatusModel):
   
    _translated_choices = [ (slug, _(name)) for(slug, name) in ptsettings.STATUS_CHOICES]
    STATUS = Choices(*_translated_choices)
    objects = QueryManager()
    public = QueryManager(status=ptsettings.STATUS_PUBLISHED)

    def _enabled(self):
        return self.status == ptsettings.STATUS_PUBLISHED
    enabled = property(_enabled)

    class Meta:
        abstract = True


class PagelikeModel(LangModel, PublishableModel, TimeStampedModel):
    title = models.CharField(u'Title', max_length=255)
    slug = UnicodeSlugField(_('Slug'), max_length=255)
    objects = models.Manager()

    def get_absolute_url(self):
        return '/%s' % self.slug

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


