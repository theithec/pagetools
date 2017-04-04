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
    def setUp(self, email_receivers=None):
        super().setUp()

        email_receivers = email_receivers or []
        self.org_receivers = pagetools.pages.forms.MAILFORM_RECEIVERS
        pagetools.pages.forms.MAILFORM_RECEIVERS = email_receivers

    def tear_down(self):
        super().tearDown()
        pagetools.pages.forms.MAILFORM_RECEIVERS = self.org_receivers

class TestContactFormMissingReceiver(ModifyMailReceiverTestCase):

    def test_sendmailform_no_reveivers(self):
        contactform = ContactForm(contactform_data)
        self.assertFalse(contactform.is_valid())

class FormsTest2Case(ModifyMailReceiverTestCase):

    def setUp(self):
        super().setUp(["q@w.de"])

    def test_sendmailform_receivers_from_settings(self):
        contactform = ContactForm(contactform_data)
        self.assertTrue(contactform.is_valid())

class FormsTest3Case(ModifyMailReceiverTestCase):
    def setUp(self):
        super().setUp(["q@w.de"])

    def test_sendmailform_overwrite_receivers(self):
        data = contactform_data
        #data['email_receivers'] = "x@y.zy"
        contactform = ContactForm(data, email_receivers="x@y.zy")
        self.assertEqual(contactform.email_receivers, ["x@y.zy"])
