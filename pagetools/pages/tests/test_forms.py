from django.test import TestCase

from pagetools.pages.forms import *


class FormsTestCase(TestCase):
    def test_sendmailform(self):
        f = SendEmailForm()
        self.assertFalse(f.is_valid())
        f = SendEmailForm({
            'email_receivers': ['q']
        })
        self.assertTrue(f.is_valid())

