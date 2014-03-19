'''
Created on 18.12.2013

@author: lotek
'''
import os

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from .settings import CONTACTFORM_RECEIVERS


class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_id = 'id-exampleForm'
        # self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
    subject = forms.CharField(max_length=100, label=_("About"), required=True)
    name = forms.CharField(label=_("Your Name"))
    sender = forms.EmailField(label=_("E-Mail"))
    message = forms.CharField(widget=forms.widgets.Textarea(), label=_("Message"))
    #cc_myself = forms.BooleanField(required=False, label=_("Kopie an mich selbst"))

    def is_valid(self, **kwargs):
        request = kwargs['request']
        _is_valid = super(ContactForm, self).is_valid()
        if _is_valid:
            from django.core.mail import send_mail
            txt = os.linesep.join([u"%s\t%s" % (field.name, field.value()) for field in self])  # _formtxt(form)
            send_mail(_("Contact"), txt, self['sender'].value(), CONTACTFORM_RECEIVERS)
            messages.add_message(request, messages.INFO, _('send ok'))
        return _is_valid
