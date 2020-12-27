import os

from django.contrib.staticfiles import finders
from django.test import TestCase

from pagetools.admin import TinyMCEMixin


class TestMediaMixin:
    """Check required static files"""

    def test_media(self):
        scripts = self.clz.Media.js
        for script in scripts:
            path = finders.find(script[8:])
            self.assertTrue(os.path.exists(path))


class TestAdminStaticFiles(TestMediaMixin, TestCase):
    def __init__(self, *args, **kwargs):
        self.clz = TinyMCEMixin
        super().__init__(*args, **kwargs)
