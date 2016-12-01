'''
Created on 18.12.2013

@author: Tim Heithecker
'''
import os

from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.forms import widgets
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .settings import MAILFORM_RECEIVERS, MAILFORM_SENDER

import logging
logger = logging.getLogger(__name__)

class DynMultipleChoiceField(forms.MultipleChoiceField):

    def __init__(self, **kwargs):
        try:
            label, values = kwargs['label'].split(':')
        except ValueError:
            raise ValidationError(
                _('ChoiceField name must be "name: option1, option2 [...])'))
        kwargs.update({
            'label': label,
            'choices': [(slugify(v), v) for v in values.split(',')],
            'widget': widgets.CheckboxSelectMultiple
        })
        super(DynMultipleChoiceField, self).__init__(**kwargs)

class MailReceiverField(object):
    help_text = _('comma separated list of e-mails')

    def __init__(self, *args, **kwargs):
        try:
            adrs = [n.strip() for n in kwargs['label'].split(',')]
            ev = EmailValidator()
            for a in adrs:
                ev(a)
        except (ValueError, ValidationError, KeyError):
            raise ValidationError(self.help_text)


'''
class BaseDynForm(forms.Form):

    def __init__(self, *args, **kwargs):
        extras = kwargs.pop('extras', [])
        kwargs.pop('extras_opt', None)
        super(BaseDynForm, self).__init__(*args, **kwargs)
        for dynfield in extras:
            self.add_custom_field(dynfield)

    def add_custom_field(self, dynfield):
        fieldkwargs = {'required': dynfield.required,
                       'label': dynfield.name}
        Fieldcls = dynfield.field_for_type.get(dynfield.field_type, None)
        if not Fieldcls:
            Fieldcls = getattr(forms, dynfield.field_type)
        extra_add = getattr(self, 'add_%s' % dynfield.field_type.lower(), None)
        if extra_add:
            extra_add(**fieldkwargs)
        else:
            fname = 'custom_%s' % slugify(dynfield.name)
            self.fields[fname] = Fieldcls(**fieldkwargs)

    def is_valid(self, **kwargs):
        _is_valid = super(BaseDynForm, self).is_valid()
        if _is_valid:
            self.msg = (messages.SUCCESS, _('Form processed'))
        else:
            self.msg = (messages.ERROR, _('An error occured'))
        return _is_valid
'''


class SendEmailForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.email_receivers = kwargs.pop('email_receivers', None)
        super(SendEmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))

    def get_mailreceivers(self):
        try:
            r = (getattr(self, 'email_receivers', "") or ",".join(MAILFORM_RECEIVERS)).split(",")
            logger.debug("Mail receivers %s " %  r)
            return r
        except AttributeError:
            logger.error("no email receivers for %s" % self)


    def is_valid(self, **kwargs):
        _is_valid = super(SendEmailForm, self).is_valid()
        if _is_valid:
            txt = os.linesep.join(
                ["%s\t%s" % (field.name, field.value())
                    for field in self
                 ])
            send_mail(_("Form"), txt, MAILFORM_SENDER,
                      self.get_mailreceivers(), fail_silently=False)
            # messages.add_message(request, messages.INFO, _('send ok'))
        return _is_valid


class ContactForm(SendEmailForm):
    subject = forms.CharField(max_length=100, label=_("About"), required=True)
    name = forms.CharField(label=_("Your Name"))
    sender = forms.EmailField(label=_("E-Mail"))
    message = forms.CharField(
        widget=forms.widgets.Textarea(), label=_("Message"))
