
'''
Created on 14.12.2013

@author: Tim Heithecker
'''

from django.contrib.auth.models import User
from django.test import TestCase
from pagetools.core.settings import STATUS_PUBLISHED
from pagetools.sections.models import PageNode, TypeMixin
from django.conf import settings

settings.IS_TEST = True



class TestNode1(PageNode):
    class Meta:
        app_label = "pagetools.sections.tests"



class ModelTests(TestCase):
    def setUp(self):
        self.n1 = TestNode1.objects.create(title="w1")

    def test_title(self):
        self.assertEqual(self.n1.title, "w1")


