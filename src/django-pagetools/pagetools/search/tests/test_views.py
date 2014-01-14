'''
Created on 20.12.2013

@author: lotek
'''

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.utils.text import slugify

from pagetools.pages.models import Page


class TC1Tests(TestCase):

    def setUp(self):
        self.client = Client()
        for title, content, is_pub in [
            (u'P%s' % i, u'Foo%s' % i, True) for i in range(4)
            
        ]:
            Page.objects.create(**{
                'title':title,
                'content': content,
                'slug': slugify(title),
                'status': u'published' if is_pub else u'draft'
            })
            
            settings.PAGINATE_BY = 3



    #def test_add_page(self):
    #    print self.client.get('http://127.0.0.1:8000/search/?s=P')
