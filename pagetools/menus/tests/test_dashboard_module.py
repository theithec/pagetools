'''
Created on 15.12.2013

@author: Tim Heithecker
'''
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.test.testcases import TestCase
from pagetools.menus.models import Menu, MenuEntry, Link
# from pagetools.menus.admin import MenuAdmin

from pagetools.menus.tests import MenuDataTestCase
from pagetools.menus.dashboard_modules import MenuModule


class DashboardTests(MenuDataTestCase):

    def setUp(self):
        super().setUp()
        self.dm = MenuModule(menu_title=self.menu.title)

    def test_admin_index(self):
        ''' test index because customdashboard with MenuModule is may used'''
        adminindex = urlresolvers.reverse('admin:index', args=[])
        response = self.client.get(adminindex, {})
        self.assertTrue(response.status_code in (200, 302))

    def test_add_entrychildren(self):
        context = {}
        self.dm.init_with_context(context)
        self.assertCountEqual(list(context.keys()), ['existing', 'menu'])
        e = context['existing']
        self.assertEqual(len(context['existing']), 4)
