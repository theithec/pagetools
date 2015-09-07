'''
Created on 15.12.2013

@author: lotek
'''
from django.test.testcases import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import (
        HORIZONTAL, VERTICAL, ModelAdmin, TabularInline,
)
from pagetools.menus.models import Menu, MenuManager, Link

class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()

class MenuAdminTests(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.menu = Menu.objects.add_root(title="menu1")
        self.l1 = Link.objects.create(title="l1", url="#")
        self.e1 = Menu.objects.add_child(self.menu,self.l1)

    #todo rf before test
    def test_change_entries_enabled(self):
        ma = ModelAdmin(Menu, self.site)
        F = ma.get_form(request, obj=self.menu)
        f = F(instance=self.menu)
