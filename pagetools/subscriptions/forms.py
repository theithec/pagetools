'''
Created on 29.02.2012

@author: lotek
'''
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


class SubscribeForm(forms.Form):
    email = forms.EmailField(label=_("E-Mail"))
    def __init__(self, *args, **kwargs):
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id="subscribeform"
        self.helper.form_action = reverse('subscriptions:subscribe')
        # i think this is wrong but  prevents empty fieldset somehow
        self.helper.layout = Layout(  'email')
        self.helper.add_input(Submit('subscribe', _('Submit')))
        self.helper.form_tag = True
