from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from pagetools.models import PagelikeModel
from .forms import ContactForm

import settings as page_settings
from pagetools.widgets.models import PageType


class IncludedForm(models.Model):
    included_form = models.CharField(max_length=255, blank=True)
    includable_forms = {_('ContaktForm'): ContactForm}
    
    def __init__(self, *args, **kwargs):
        super(IncludedForm, self).__init__(*args, **kwargs)
        self._meta.get_field_by_name('included_form')[0]._choices = [
            (i, i) for i in self.includable_forms.keys()
        ]
        
    class Meta:
        abstract = True
    

class AuthPage(models.Model):
    login_required = models.BooleanField(_('Login required'), default=False)

    class Meta:
        abstract = True


class BasePage(IncludedForm, AuthPage, PagelikeModel):
    content = models.TextField(u'Content')
    objects = models.Manager()
    pagetype = models.ForeignKey(PageType, blank=True, null=True)
    
    def get_pagetype(self, *kwargs):
        return self.pagetype
    
    def get_absolute_url(self):
        return u'/%s%s' % (page_settings.PAGE_PREFIX, self.slug)

    class Meta(PagelikeModel.Meta):
        verbose_name = u'Page'
        abstract = True
class Page(BasePage):
    pass
    
        
# 
class PageBlockMixin(models.Model):
    content = models.TextField(_(u'Content'), blank=True)
    visible = models.BooleanField(_(u'Visible'), default=True)
    # in concrete model:
    # page = models.ForeignKey(MyBlockPage)
    position = models.PositiveIntegerField()

    class Meta:
        verbose_name = u"Block"
        ordering = ('position',)

    def __unicode__(self):
        lc = len(self.content)
        sc = strip_tags(self.content) or self.content
        return sc[:100 if lc > 100 else lc]
