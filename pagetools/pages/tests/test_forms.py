from django import forms
from django.test import TestCase

from pagetools.pages.forms import *


class TestForm(SendEmailForm):
    dmcf = DynMultipleChoiceField(label="dmcf: 1,2,3")


class FormsTestCase(TestCase):
    def test_sendmailform(self):
        f = TestForm()
        self.assertFalse(f.is_valid())
        f = TestForm({
            'email_receivers': ['q'],
            'dmcf': ["1", "2"]
        })
        self.assertTrue(f.is_valid())
        f = TestForm({
            'email_receivers': ['q'],
            'dmcf': ["1", "2"]
        })

    def testBadDyn(self):
        self.assertRaises(
            ValidationError,
            lambda: DynMultipleChoiceField(label="sowrong"))
