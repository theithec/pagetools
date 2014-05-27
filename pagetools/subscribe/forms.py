'''
Created on 29.02.2012

@author: lotek
'''
from django.utils.translation import ugettext_lazy as _

from django import forms


class SubscribeForm(forms.Form):
    email = forms.EmailField(label=_("E-Mail"))

