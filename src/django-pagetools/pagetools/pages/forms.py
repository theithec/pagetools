'''
Created on 18.12.2013

@author: lotek
'''
import os

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from .settings import MAILFORM_RECEIVERS
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class BaseDynForm(forms.Form):

    def __init__(self, *args, **kwargs):
        extras = kwargs.pop('extras', [])
        super(BaseDynForm, self).__init__(*args, **kwargs)
        
        for i, dynfield in enumerate(extras):
            print i, dynfield.__dict__
            self.add_custom_field(dynfield)
            
    
    def add_custom_field(self, dynfield):
        fieldkwargs = {'required':dynfield.required}
        Fieldcls = None
        if dynfield.field_type == 'ChoiceField':
            try:
                label, values = dynfield.name.split(':')
            except ValueError:
                raise ValidationError('ChoiceField name must be "name: option1, option2 [...]')
            
            fieldkwargs['label'] = label
            fieldkwargs['choices'] = [(slugify(v),v) for v in values.split(',')]
            fieldkwargs['widget'] = widgets.CheckboxSelectMultiple
            Fieldcls = forms.MultipleChoiceField
        else:
            fieldkwargs['label'] = dynfield.name
            Fieldcls = getattr(forms, dynfield.field_type )
            
            #self.fields['custom_%s' % slugify(dynfield.name)] = forms.MultipleChoiceField(label=label,choices=choices, widget=widgets.CheckboxSelectMultiple)
        self.fields['custom_%s' % slugify(dynfield.name)] = Fieldcls(**fieldkwargs)
    
    
    def is_valid(self, **kwargs):
        _is_valid =  super(BaseDynForm, self).is_valid()
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
        _is_valid = super(SendEmailForm, self).is_valid()
        if _is_valid:
            from django.core.mail import send_mail
            txt = os.linesep.join([u"%s\t%s" % (field.name, field.value()) for field in self])  # _formtxt(form)
            send_mail(_("Form"), txt, "lotek@localhost", MAILFORM_RECEIVERS, fail_silently=False)

            #send_mail(_("Form"), txt, self['sender'].value(), MAILFORM_RECEIVERS, fail_silently=False)
            #messages.add_message(request, messages.INFO, _('send ok'))
        return _is_valid


class ContactForm(SendEmailForm):
    subject = forms.CharField(max_length=100, label=_("About"), required=True)
    name = forms.CharField(label=_("Your Name"))
    sender = forms.EmailField(label=_("E-Mail"))
    message = forms.CharField(widget=forms.widgets.Textarea(), label=_("Message"))
    #cc_myself = forms.BooleanField(required=False, label=_("Kopie an mich selbst"))

