'''
Created on 14.12.2013

@author: Tim Heithecker
'''

from django.test import TestCase

from pagetools.menus.models import Menu, Link
from pagetools.menus.templatetags.menus_tags import MenuRenderer
from pagetools.pages.models import Page


class TemplatetagsTests(TestCase):

    def setUp(self):
        self.menu = Menu.objects.add_root(title='m1')
        self.menu.save()
        self.p1 = Page.objects.create(title='P1', slug='p1')
        self.e1 = self.menu.children.add_child(self.p1, enabled=True)
        self.l1 = Link.objects.create(url='/foo')
        self.e2 = self.menu.children.add_child(self.l1, enabled=True)
        self.menu.update_cache()

    def test_entries(self):
        mr = MenuRenderer('foo', 'm1').render({})
        self.assertTrue(self.l1.url in mr)
        self.assertFalse(self.p1.slug in mr)
        self.p1.status = 'published'
        self.p1.save()
        self.menu.update_cache()
        mr = MenuRenderer('foo', 'm1').render({})
        self.assertTrue(self.p1.slug in mr)

    def test_hidden_subentries(self):

        self.l3 = Link.objects.create(url='/foo3')
        self.e3 = self.e2.children.add_child(self.l3, enabled=False)

        mr = MenuRenderer('foo', 'm1').render({})
        self.assertNotIn("/foo3", mr)
