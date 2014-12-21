'''
Created on 14.12.2013

@author: lotek
'''

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from django.contrib import auth
from pagetools.core.settings import STATUS_PUBLISHED
from pagetools.pages.models import Page
from pagetools.pages.forms import ContactForm

class FormTests(TestCase):
    def setUp(self):
        f = ContactForm()
        #e = EMail


    def test_title(self):
        pass #self.assertEqual(self.page.title, 'p1')
