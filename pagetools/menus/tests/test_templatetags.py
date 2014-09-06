'''
Created on 14.12.2013

@author: lotek
'''

from django.test import TestCase

from pagetools.menus.models import Menu, Link
from pagetools.menus.templatetags.menus_tags import MenuRenderer
from pagetools.pages.models import Page


class TC1Tests(TestCase):

    def setUp(self):
        self.menu = Menu.tree.add_root(title='m1')
        self.menu.save()
        print(("MENU", self.menu))
        self.p1 = Page.objects.create(title='P1', slug='p1')
        self.e1 = Menu.tree.add_child(self.menu, self.p1, enabled=True)
        self.l1 = Link.objects.create(url='/foo')
        self.e2 = Menu.tree.add_child(self.menu, self.l1, enabled=True)
        self.menu.update_cache()

    def test_entries(self):
        mr = MenuRenderer('foo', 'm1').render({})
        print()
        print("MR")
        print(mr)
        print()
        self.assertTrue(self.l1.url in mr)
        self.assertFalse(self.p1.slug in mr)
        self.p1.status = 'published'
        print(("P1\n", self.p1.__dict__))
        print((Page.objects.all()))
        self.p1.save()
        self.menu.update_cache()
        mr = MenuRenderer('foo', 'm1').render({})
        self.assertTrue(self.p1.slug in mr)
