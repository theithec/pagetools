import os
from django.test import TestCase
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
import django.conf

from pagetools.core.admin import *

class TestMediaMixin(object):
    """Check required static files"""

    def test_media(self):
        js = self.clz.Media.js
        for f in js:
            p = finders.find(f[8:])
            # self.assertTrue(staticfiles_storage.exists(p))
            self.assertTrue(os.path.exists(p))


class TestAdminStaticFiles(TestMediaMixin, TestCase):
    def __init__(self, *args, **kwargs):
        self.clz = TinyMCEMixin
        super().__init__(*args, **kwargs)

'''
# too complicated
from .seleniumtestcase import SeleniumTestCase

class AdminTest(SeleniumTestCase):

    def test_media(self):
        bad_path = "/MEMUSTNOTEXIST"
        not_found = "The requested URL %s was not found on this server."
        response = self.browser.get(self.live_server_url + bad_path )
        t1 = self.browser.find_element_by_tag_name("body").text
        self.assertTrue(not_found % bad_path in t1)
        js = TinyMCEMixin.Media.js
        for f in js:
            request = self.browser.get(self.live_server_url + f)
            t1 = self.browser.find_element_by_tag_name("body").text
            self.assertFalse(not_found % f in t1)
'''




