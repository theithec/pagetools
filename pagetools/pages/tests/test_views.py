'''
Created on 15.12.2013

@author: Tim Heithecker
'''

from pagetools.menus.tests import MenuDataTestCase
import pagetools.pages.models
from pagetools.pages.forms import ContactForm

from django.test import override_settings

from .test_forms import ModifyMailReceiverTestCase

class PageViewTestCase(ModifyMailReceiverTestCase, MenuDataTestCase):

    def setUp(self):
        super().setUp(["q@w.de"])

    def test_detailview(self):
        response = self.client.get(self.p1.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    # ? does not work @override_settings(CAPTCHA_TEST_MODE=True)
    def test_with_form(self):
            import captcha.conf.settings
            captcha.conf.settings.CAPTCHA_TEST_MODE = True
            data = {
                'sender': 'x@y.de',
                'name': 'Name',
                'message': 'The Message',
                'content': 'Content',
                'subject': 'Subject',
                'captcha_0': 'xPASSED',
                'captcha_1': 'PASSED',

            }
            pagetools.pages.models.Page.includable_forms = {'Contactform': ContactForm}
            r = self.client.post(self.p1.get_absolute_url(), data)
            self.assertEqual(r.status_code, 200)
            self.assertNotContains(r, "An error occured")

            data.pop('sender')
            r = self.client.post(self.p1.get_absolute_url(), data)
            self.assertEqual(r.status_code, 200)
            self.assertContains(r, "error_1_id_sender")
