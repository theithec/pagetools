from django import forms
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from pagetools.core.models import PagelikeModel
from pagetools.widgets.models import PageType
import settings as page_settings

from .forms import ContactForm, DynMultipleChoiceField, MailReceiverField


class IncludedForm(models.Model):
    included_form = models.CharField(
        _("Included form"), max_length=255, blank=True)
    includable_forms = {'ContaktForm': ContactForm}

    def __init__(self, *args, **kwargs):
        super(IncludedForm, self).__init__(*args, **kwargs)
        self._meta.get_field_by_name('included_form')[0]._choices = [
            (i, _(i)) for i, j in self.includable_forms.items()
        ]

    class Meta:
        abstract = True


class DynFormField(models.Model):

    field_for_type = {
        u'ChoiceField': DynMultipleChoiceField,
        u'MailReceiverField': MailReceiverField
    }
    field_type = models.CharField('Type', max_length=128)
    name = models.CharField(_('Name'), max_length=512)
    required = models.BooleanField(_('required'))
    position = models.PositiveSmallIntegerField("Position")
    help_text = models.CharField(_('Helptext'), max_length=512, blank=True)
    initial = models.CharField(_('Default'), max_length=512, blank=True)
    form_containing_model = None
    # models.ForeignKey(ConcrteIncludedForm, related_name='dynformfields')

    def __init__(self, *args, **kwargs):
        super(DynFormField, self).__init__(*args, **kwargs)
        self._meta.get_field_by_name('field_type')[0]._choices = self.get_fieldchoices()

    def get_fieldchoices(self):
        return (('CharField', _('TextField')),
                ('EmailField', _('EmailField')),
                ('ChoiceField', _('ChoiceField')),
                ('BooleanField', _('CheckField')),
                ('MailReceiverField', _('MailReceiverField'))
                )

    def clean(self):
        pass

    def to_field(self):
        Fieldcls = self.field_for_type.get(self.field_type, None)
        if not Fieldcls:
            Fieldcls = getattr(forms, self.field_type)
        return Fieldcls(label=self.name, required=self.required,
                        help_text=self.help_text, initial=self.initial)

    def __unicode__(self):
        return u'%s: %s' % (self.field_type, self.name)

    class Meta:
        verbose_name = _('Dynamic Form Field')
        verbose_name_plural = _('Dynamic Form Fields')
        ordering = ['position']
        abstract = True


class AuthPage(models.Model):
    login_required = models.BooleanField(_('Login required'), default=False)

    class Meta:
        abstract = True


class BasePage(IncludedForm, AuthPage, PagelikeModel):
    content = models.TextField(_('Content'))
    #objects = models.Manager()
    pagetype = models.ForeignKey(PageType, blank=True, null=True)

    def get_pagetype(self, **kwargs):
        return self.pagetype

    def get_absolute_url(self):
        return reverse('pageview', kwargs={'slug': self.slug})

    class Meta(PagelikeModel.Meta):
        verbose_name = _('Page')
        abstract = True


class Page(BasePage):
    pass


class PageDynFormField(DynFormField):
    form_containing_model = models.ForeignKey(Page,
                                              related_name='dynformfields')


class PageBlockMixin(models.Model):
    content = models.TextField(_('Content'), blank=True)
    visible = models.BooleanField(_(u'Visible'), default=True)
    # in concrete model:
    # page = models.ForeignKey(MyBlockPage)
    position = models.PositiveIntegerField()

    class Meta:
        verbose_name = u"Block"
        ordering = ('position',)
        abstract = True

    def __unicode__(self):
        lc = len(self.content)
        sc = strip_tags(self.content) or self.content
        return sc[:100 if lc > 100 else lc]
