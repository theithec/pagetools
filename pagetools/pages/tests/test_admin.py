'''
Created on 15.12.2013

@author: lotek
'''
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.test.client import Client
from django.test.testcases import TestCase

from django.utils.text import slugify


class Tests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser('admin', 'q@w.de', 'alice')
        self.addpageurl = urlresolvers.reverse('admin:pages_page_add', args=[])
        self.pages_data = [
            ('P1', 'Foo', True),
            # s (u'P2', u'Bar', False, u'pp2')
        ]

    def _add_page(self, args):
        title, content = args[:2]
        status = 'published' if args[2] else 'draft'
        slug = slugify(title) if len(args) < 4 else args[3]
        response = self.client.post(
            self.addpageurl,
            {'title': title,
             'slug': slug,
             'content': content,
             'status': status,
             'dynformfields-TOTAL_FORMS': 1,
             'dynformfields-INITIAL_FORMS': 0
             }
        )
        return response.status_code

    def test_add_page(self):
        self.client.login(username="admin", password='password')
        for data in self.pages_data:
            c = self._add_page(data)
            self.assertTrue(c in (200, 302))
