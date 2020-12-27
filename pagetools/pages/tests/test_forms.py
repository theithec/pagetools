from unittest import mock
from django.test import TestCase

from pagetools.pages.forms import ContactForm

CONTACTFORM_DATA = {
    "subject": "Test",
    "sender": "q@w.de",
    "message": "Foo",
    "name": "Name",
}


class TestContactFormMissingReceiver(TestCase):
    @mock.patch("pagetools.pages.forms.MAILFORM_RECEIVERS", [])
    def test_sendmailform_no_reveivers(self, *_args):
        contactform = ContactForm(CONTACTFORM_DATA)
        self.assertFalse(contactform.is_valid())


class TestContactFormWithSettingsReceiver(TestCase):
    @mock.patch("pagetools.pages.forms.MAILFORM_RECEIVERS", ["q@w.de"])
    def test_sendmailform_receivers_from_settings(self, *_args):
        contactform = ContactForm(CONTACTFORM_DATA)
        self.assertTrue(contactform.is_valid())


class TestContactFormWithKwargReceiver(TestCase):
    def test_sendmailform_overwrite_receivers(self):
        data = CONTACTFORM_DATA
        contactform = ContactForm(data, mailreceivers=["x@y.zy"])
        self.assertEqual(contactform.mailreceivers, ["x@y.zy"])
