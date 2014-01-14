'''
Created on 14.12.2013

@author: lotek
'''

from django.test import TestCase

from pagetools.menus.models import Menu, MenuEntry, Link, MenuManager
from pagetools.pages import settings
from pagetools.pages.models import Page
from django.core.exceptions import ValidationError
from pagetools.settings import STATUS_PUBLISHED


class TC1Tests(TestCase):

    def setUp(self):
        self.menu = Menu.tree.add_root(title='m1',)
        self.p1 = Page.objects.create(title='P1', slug='p1', status=STATUS_PUBLISHED)
        self.e1 = Menu.tree.add_child(self.menu, self.p1)
        self.l1 = Link.objects.create(url='/foo')
        self.e2 = Menu.tree.add_child(self.menu, self.l1)

    def test_validation(self):
        self.assertRaises(ValidationError, Menu.tree.add_child, self.menu, self.p1)

    def test_lists(self):
        c = self.menu.get_children()
        self.assertEqual(self.menu.title, u'm1')
        self.assertEqual(
            c[0].get_absolute_url(),
            u'/%sp1' % settings.PAGE_PREFIX
        )
        self.assertEqual(
           c[1].get_absolute_url(),
            u'/foo'
        )
  

