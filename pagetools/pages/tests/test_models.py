'''
Created on 14.12.2013

@author: lotek
'''

from django.test import TestCase
from django.test.client import Client

from pagetools.pages.models import Page
from pagetools.core.settings import STATUS_PUBLISHED

class TC1Tests(TestCase):

    def setUp(self):
        self.page = Page.objects.get_or_create(title='p1', slug="p1")[0]

    def test_lists(self):
        self.assertEqual(self.page.title, 'p1')

    def test_status(self):
        self.assertEqual(self.page.status, 'draft')
        c = Client()
        resp = c.get(self.page.get_absolute_url())
        self.assertEqual(resp.status_code, 404)

        self.page.status = STATUS_PUBLISHED
        self.page.save()
        resp = c.get(self.page.get_absolute_url())
        self.assertEqual(resp.status_code, 200)
