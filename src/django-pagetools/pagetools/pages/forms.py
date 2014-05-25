'''
Created on 18.12.2013

@author: lotek
'''
import os

from django import forms
from django.contrib import messages
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .settings import MAILFORM_RECEIVERS, MAILFORM_SENDER

class DynMultipleChoiceField(forms.MultipleChoiceField):
    
    def __init__(self, **kwargs):
        try:
            label, values = kwargs['label'].split(':')
        except ValueError:
            raise ValidationError('ChoiceField1 name must be "name: option1, option2 [...]')
        kwargs.update({
            'label': label,
            'choices': [(slugify(v), v) for v in values.split(',')],
            'widget': widgets.CheckboxSelectMultiple
        })
        super(DynMultipleChoiceField, self).__init__(**kwargs)
        


class BaseDynForm(forms.Form):

    def __init__(self, *args, **kwargs):
        extras = kwargs.pop('extras', [])
        super(BaseDynForm, self).__init__(*args, **kwargs)
        
        for i, dynfield in enumerate(extras):
            self.add_custom_field(dynfield)
            
    
    def add_custom_field(self, dynfield):
        fieldkwargs = {'required':dynfield.required,
                       'label': dynfield.name}
        Fieldcls = dynfield.field_for_type.get(dynfield.field_type, None)
        if not Fieldcls:
            Fieldcls = getattr(forms, dynfield.field_type)
       
            
            # self.fields['custom_%s' % slugify(dynfield.name)] = forms.MultipleChoiceField(label=label,choices=choices, widget=widgets.CheckboxSelectMultiple)
        self.fields['custom_%s' % slugify(dynfield.name)] = Fieldcls(**fieldkwargs)
    
    
    def is_valid(self, **kwargs):
        _is_valid = super(BaseDynForm, self).is_valid()
        if _is_valid:
            self.msg = (messages.SUCCESS, _('Form processed'))
        else:
            self.msg = (messages.ERROR, _('An error occured'))
        return _is_valid



class SendEmailForm(BaseDynForm):
    
    def __init__(self, *args, **kwargs):
        super(SendEmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    def is_valid(self, **kwargs):
        # call super.super to  not to send in super.is_valid
        _is_valid = super(SendEmailForm, self).is_valid()
        if _is_valid:
            txt = os.linesep.join([u"%s\t%s" % (field.name, field.value()) for field in self])  # _formtxt(form)
            send_mail(_("Form"), txt, MAILFORM_SENDER, MAILFORM_RECEIVERS, fail_silently=False)

            # send_mail(_("Form"), txt, self['sender'].value(), MAILFORM_RECEIVERS, fail_silently=False)
            # messages.add_message(request, messages.INFO, _('send ok'))
        return _is_valid


class ContactForm(SendEmailForm):
    subject = forms.CharField(max_length=100, label=_("About"), required=True)
    name = forms.CharField(label=_("Your Name"))
    sender = forms.EmailField(label=_("E-Mail"))
    message = forms.CharField(widget=forms.widgets.Textarea(), label=_("Message"))
    # cc_myself = forms.BooleanField(required=False, label=_("Kopie an mich selbst"))

