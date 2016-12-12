'''
Created on 14.12.2013

@author: Tim Heithecker
'''



from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.translation import get_language

from pagetools.core.settings import STATUS_PUBLISHED
from pagetools.menus.models import Menu, MenuEntry, Link, MenuManager
from pagetools.pages import settings
from pagetools.pages.models import Page

from pagetools.menus.tests import MenuDataTestCase

class ModelTests(MenuDataTestCase):


    def test_validation(self):
        self.assertRaises(
            ValidationError,
            self.menu.children.add_child, self.p1)

    def test_rm_and_add_again(self):
        self.e_p1.delete()
        self.menu.save()
        self.e_p1 = self.menu.children.add_child(self.p1)

    def test_childen(self):
        lang = get_language()
        c = self.menu.get_children()
        self.assertEqual(self.menu.title, 'MainMenu')
        u0 = c[0].get_absolute_url()
        if u0.startswith("/%s/" % lang ):
            u0 = u0[3:]
        u1 = c[1].get_absolute_url()
        if u1.startswith("/%s/" % lang):
            u1 = u0[3:]
        self.assertEqual(
            u1,
            self.p1.get_absolute_url()
        )
        self.assertEqual(self.e_v1.get_absolute_url(), "/")

    def test_entry_slugs(self):
        self.assertEqual(self.e_p1.slug, "start")

    def test_renamed_entry_slugs(self):
        self.p1.slug = "P1"
        self.p1.save()
        self.menu.save()
        self.assertEqual(self.menu.get_children()[1].slug, "P1")


    def test_doubleslug(self):
        with self.assertRaises(ValidationError):
            self.menu.children.add_child(self.p1)

class M2Tests(TestCase):
    def test_create(self):
        m = Menu.objects.add_root("M1")
        p = Page.objects.create(title="t1", slug="t1", content="t1", status="published")
        m.children.add_child(p)
        self.assertEqual(p, m.children.first().content_object)

