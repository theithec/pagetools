'''
Created on 15.12.2013

@author: Tim Heithecker
'''
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.test.testcases import TestCase
from pagetools.menus.models import Menu, MenuEntry, Link
# from pagetools.menus.admin import MenuAdmin

from pagetools.menus.dashboard_modules import MenuModule



class DashboardTests(TestCase):

    def setUp(self):
        self.dm = MenuModule()

    def test_admin_index(self):
        ''' test index because customdashboard with MenuModule is may used'''
        adminindex = urlresolvers.reverse('admin:index', args=[])
        response = self.client.get(adminindex, {})
        self.assertTrue(response.status_code in (200, 302))

    def test_add_entrychildren(self):
       collected = self.dm.add_entrychildren({})
       self.assertEqual(len(collected), 0)

