from django import forms
from django.test import TestCase, modify_settings


from pagetools.pages.forms import ContactForm, MAILFORM_RECEIVERS

import pagetools.pages.forms

contactform_data = {
    "subject": "Test",
    "sender": "q@w.de",
    "message": "Foo",
    "name": "Name"
}


class ModifyMailReceiverTestCase(TestCase):
    def setUp(self, mailreceivers=None):
        super().setUp()

        mailreceivers = mailreceivers or []
        self.org_receivers = pagetools.pages.forms.MAILFORM_RECEIVERS
        pagetools.pages.forms.MAILFORM_RECEIVERS = mailreceivers

    def tear_down(self):
        super().tearDown()
        pagetools.pages.forms.MAILFORM_RECEIVERS = self.org_receivers


class TestContactFormMissingReceiver(ModifyMailReceiverTestCase):

    def test_sendmailform_no_reveivers(self):
        contactform = ContactForm(contactform_data)
        self.assertFalse(contactform.is_valid())


class TestContactFormWithSettingsReceiver(ModifyMailReceiverTestCase):

    def setUp(self):
        super().setUp(["q@w.de"])

    def test_sendmailform_receivers_from_settings(self):
        contactform = ContactForm(contactform_data)
        self.assertTrue(contactform.is_valid())


class TestContactFormWithKwargReceiver(ModifyMailReceiverTestCase):
    def setUp(self):
        super().setUp(["q@w.de"])

    def test_sendmailform_overwrite_receivers(self):
        data = contactform_data
        contactform = ContactForm(data, mailreceivers=["x@y.zy"])
        self.assertEqual(contactform.mailreceivers, ["x@y.zy"])
