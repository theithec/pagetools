
'''
Created on 14.12.2013

@author: Tim Heithecker
'''

from django.contrib.auth.models import User
from django.test import TestCase
from pagetools.core.settings import STATUS_PUBLISHED
from pagetools.pages.models import Page
from django.conf import settings
settings.IS_TEST = True


from pagetools.sections.models import PageNode

class TestNode(PageNode):
    pass
    class Meta:
        app_label = "pagetools.sections.tests"
class TC1Tests(TestCase):
    def setUp(self):
        self.n = TestNode.objects.create(title="w")
    def test_title(self):
        self.assertEqual(self.n.title, "w")
