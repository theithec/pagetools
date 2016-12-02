'''
Created on 20.12.2013

@author: Tim Heithecker
'''

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.utils.text import slugify

from pagetools.pages.models import Page


class SearchViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        for title, content, is_pub in [
            ('P%s' % i, 'Foo%s' % i, True) for i in range(4)

        ]:
            Page.objects.create(**{
                'title':title,
                'content': content,
                'slug': slugify(title),
                'status': 'published' if is_pub else 'draft'
            })

            settings.PAGINATE_BY = 3


    def test_search4page(self):
        response = self.client.get('/search/?contains_all=Foo1')
        self.assertTrue("P1" in str(response.content))
        self.assertFalse("P2" in str(response.content))

        response = self.client.get('/search/?contains_any=Foo1 Foo2')
        self.assertTrue("P1" in str(response.content))
        self.assertTrue("P2" in str(response.content))
        self.assertFalse("P3" in str(response.content))
