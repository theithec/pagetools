'''Models (mostly) for pages.

@author Tim Heithecker
'''
import django
from django import forms
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from pagetools.core.models import PagelikeModel
from pagetools.core.utils import choices2field
from pagetools.widgets.models import PageType

from .forms import ContactForm, CaptchaContactForm, MailReceiverField #  , DynMultipleChoiceField


class IncludedForm(models.Model):
    '''Mixin to include a choosable form to an object

    The forms are defined in ``includeable_forms`` like
    {stringkey: <Class>, ...}
    '''

    included_form = models.CharField(
        _("Included form"), max_length=255, blank=True, choices=(('dummy', 'dummy'),))
    includable_forms = {
        'Contactform': ContactForm,
        'Contactfrom(Captcha)':  CaptchaContactForm,
    }

    def __init__(self, *args, **kwargs):
        '''
        Args:
            included_form(django.db.models.CharField)
        '''

        super(IncludedForm, self).__init__(*args, **kwargs)
        #self._meta.get_field_by_name('included_form')[0]._choices = [
        choices = [
            (i, _(i)) for i, j in list(self.includable_forms.items())]
        choices2field(self._meta.get_field('included_form'), choices)

    class Meta:
        abstract = True


class IncludedEmailForm(IncludedForm):
    email_receivers = models.CharField(
        _("Email Receivers"),
        max_length=512,
        blank=True,
        help_text="Comma separated list of emails")

    class Meta:
        abstract = True

'''
class DynFormField(models.Model):

    field_for_type = {
        'ChoiceField': DynMultipleChoiceField,
        'MailReceiverField': MailReceiverField
    }
    field_type = models.CharField(
        'Type',
        max_length=128,
        help_text=_('The type of the field (e.g. textfield)')
    )
    name = models.CharField(
        _('Value'),
        max_length=512,
        help_text=_('The visible name of the field')
    )
    required = models.BooleanField(
        _('required'),
        default=False,
        help_text=_('Is the field required?'))
    position = models.PositiveSmallIntegerField("Position")
    help_text = models.CharField(
        _('Helptext'),
        max_length=512,
        blank=True,
        help_text='The helptext of the field ')
    initial = models.CharField(
        _('Default'),
        max_length=512,
        blank=True,
        help_text=_('The default value of the field')
    )
    form_containing_model = None
    # models.ForeignKey(ConcrteIncludedForm, related_name='dynformfields')

    def __init__(self, *args, **kwargs):
        super(DynFormField, self).__init__(*args, **kwargs)
        self._meta.get_field_by_name(
            'field_type')[0]._choices = self.get_fieldchoices()

    def get_fieldchoices(self):
        return (
            ('CharField', "%s#%s" % (_('TextField'), "A field to enter text")),
            ('EmailField', _('EmailField')),
            ('ChoiceField', _('ChoiceField')),
            ('BooleanField', _('CheckField')),
        )

    def clean(self):
        # self.to_field().clean()?
        pass

    def to_field(self):
        Fieldcls = self.field_for_type.get(self.field_type, None)
        if not Fieldcls:
            Fieldcls = getattr(forms, self.field_type)
            return Fieldcls(label=self.name, required=self.required,
                            help_text=self.help_text, initial=self.initial)

    def __str__(self):
        return '%s: %s' % (self.field_type, self.name)

    class Meta:
        verbose_name = _('Dynamic Form Field')
        verbose_name_plural = _('Dynamic Form Fields')
        ordering = ['position']
        abstract = True
'''

class AuthPage(models.Model):
    login_required = models.BooleanField(_('Login required'), default=False)

    class Meta:
        abstract = True


class BasePage(IncludedEmailForm, AuthPage, PagelikeModel):
    '''A basemodel for a page with one main content area

    Args:
        content(django.db.models.TextField)

        pagetype(pagetools.widgets.models.Pagetype)
    '''
    content = models.TextField(_('Content'))
    objects = models.Manager()
    pagetype = models.ForeignKey(PageType, blank=True, null=True)
    '''See :class:`pagetools.widgets.models.PageType`
    '''

    def get_pagetype(self, **kwargs):
        return self.pagetype

    def get_absolute_url(self):
        return reverse('pages:pageview', kwargs={'slug': self.slug})

    class Meta(PagelikeModel.Meta):
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        unique_together = ("slug", "lang")
        abstract = True


class Page(BasePage):
    pass

'''
class PageDynFormField(DynFormField):
    form_containing_model = models.ForeignKey(
        Page,
        related_name='dynformfields',
        help_text='Additional fields and settings for the included form')

    class Meta:
        verbose_name = _("Form field")
        verbose_name_plural = _("Additional form fields")
'''

class PageBlockMixin(models.Model):
    content = models.TextField(_('Content'), blank=True)
    visible = models.BooleanField(_('Visible'), default=True)
    # in concrete model:
    # page = models.ForeignKey(MyBlockPage)
    position = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Block"
        ordering = ('position',)
        abstract = True

    def __str__(self):
        lc = len(self.content)
        sc = strip_tags(self.content) or self.content
        return sc[:100 if lc > 100 else lc]
