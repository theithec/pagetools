'''
Created on 14.12.2013

@author: lotek
'''

from django.test import TestCase

from pagetools.pages.models import Page


class TC1Tests(TestCase):

    def setUp(self):
        self.page = Page.objects.get_or_create(title='p1')[0]

    def test_lists(self):
        self.assertEqual(self.page.title, 'p1')
 
