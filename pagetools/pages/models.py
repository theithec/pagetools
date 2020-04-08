'''Models (mostly) for pages.'''
from django.urls import reverse
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from pagetools.core.models import PagelikeModel
from pagetools.widgets.models import PageType


from .forms import ContactForm, CaptchaContactForm


class IncludedForm(models.Model):
    '''Mixin to include a choosable form to an object

    The forms are defined in ``includeable_forms`` like
    {stringkey: <Class>, ...}
    '''

    included_form = models.CharField(
        _("Included form"), max_length=255, blank=True, choices=(
            ('dummy', 'dummy'),))
    includable_forms = {
        'Contactform': ContactForm,
        'Contactfrom(Captcha)': CaptchaContactForm,
    }

    def __init__(self, *args, **kwargs):
        '''
        Args:
            included_form(django.db.models.CharField)
        '''

        super(IncludedForm, self).__init__(*args, **kwargs)
        choices = [
            (i, _(i)) for i, j in list(self.includable_forms.items())]
        self._meta.get_field('included_form').choices = choices

    class Meta:
        abstract = True


class IncludedEmailForm(IncludedForm):
    email_receivers = models.CharField(
        _("Email Receivers"),
        max_length=512,
        blank=True,
        help_text="Comma separated list of emails")

    def email_receivers_list(self):
        return [part.strip() for part in self.email_receivers.split(",") if part.strip()]

    class Meta:
        abstract = True


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
    pagetype = models.ForeignKey(PageType, blank=True, null=True, on_delete=models.CASCADE)
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
    objects = models.Manager()


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
        content_len = len(self.content)
        stripped = strip_tags(self.content) or self.content
        return stripped[:100 if content_len > 100 else content_len]
