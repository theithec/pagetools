'''
Created on 15.12.2013

@author: lotek
'''
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.test.client import Client
from django.test.testcases import TestCase

from pagetools.pages.models import Page
from django.utils.text import slugify


class Tests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser('admin', 'q@w.de', 'alice')
        self.addpageurl = urlresolvers.reverse('admin:pages_page_add', args=[])
        self.pages_data = [
            (u'P1', u'Foo', True),
            (u'P2', u'Bar', False, u'pp2')
        ]

    def _add_page(self, args):
        title, content = args[:2]
        status = u'published' if args[2] else u'draft'
        slug = slugify(title) if len(args) < 4 else args[3]
        response = self.client.post(
            self.addpageurl,
            {'title': title,
             'slug': slug,
             'content': content,
             'status': status}
        )
        return response.status_code

    def test_add_page(self):
        self.client.login(username="admin", password='alice')
        for data in self.pages_data:
            c = self._add_page(data)
            self.assertEqual(c, 302)
