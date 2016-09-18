'''
Created on 15.12.2013

@author: Tim Heithecker
'''
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.test.testcases import TestCase
from pagetools.menus.models import Menu
from pagetools.menus.admin import MenuAddForm


class MenuAdminTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'q@w.de', 'password')
        self.client.login(username="admin", password='password')

    def test_admin_index(self):
        ''' test index because customdashboard with MenuModule is may used'''
        adminindex = urlresolvers.reverse('admin:index', args=[])
        response = self.client.get(adminindex, {})
        self.assertTrue(response.status_code in (200, 302))

    def test_menu_addform(self):
        mf = MenuAddForm( {'title':'Testmenu1'})
        print ("MENU ADD", mf.clean)

    def test_add_menu(self):
        menuaddurl = urlresolvers.reverse('admin:menus_menu_add', args=[])
        response = self.client.post(menuaddurl, {'title':'Testmenu1'})
        print ("MENU ADD", response.status_code)
        self.assertTrue(response.status_code in (200, 302))
