'''
Created on 14.12.2013

@author: lotek
'''

from django.test import TestCase

from pagetools.menus.models import Menu, MenuEntry, Link, MenuManager
from pagetools.pages import settings
from pagetools.pages.models import Page
from django.core.exceptions import ValidationError
from pagetools.core.settings import STATUS_PUBLISHED
from django.utils.translation import get_language


class TC1Tests(TestCase):

    def setUp(self):
        self.menu = Menu.objects.add_root(title='m1',)
        self.p1 = Page.objects.create(title='P1', slug='p1', status=STATUS_PUBLISHED)
        self.e1 = Menu.objects.add_child(self.menu, self.p1)
        self.l1 = Link.objects.create(url='/foo')
        self.e2 = Menu.objects.add_child(self.menu, self.l1)

    def test_validation(self):
        self.assertRaises(ValidationError, Menu.objects.add_child, self.menu, self.p1)

    def test_rm_and_add_again(self):
        self.e1.delete()
        self.menu.save()
        self.e1 = Menu.objects.add_child(self.menu, self.p1)

    def test_lists(self):
        lang = get_language()
        c = self.menu.get_children()
        self.assertEqual(self.menu.title, 'm1')
        u0 = c[0].get_absolute_url()
        if u0.startswith("/%s/" % lang ):
            u0 = u0[3:]
        u1 = c[1].get_absolute_url()
        if u1.startswith("/%s/" % lang):
            u1 = u0[3:]
        self.assertEqual(
            u1,
            '/foo'
        )

    def test_entry_slugs(self):
        self.assertEqual(self.e1.slug, "p1")

    def test_renamed_entry_slugs(self):
        self.p1.slug = "P1"
        self.p1.save()
        self.menu.save()
        self.assertEqual(self.menu.get_children()[0].slug, "P1")

