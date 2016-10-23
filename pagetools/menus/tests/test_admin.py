'''
Created on 15.12.2013

@author: Tim Heithecker
'''
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.test.testcases import TestCase
from pagetools.menus.models import Menu, Link
from pagetools.menus.admin import MenuAddForm, MenuChangeForm


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


    def test_dublicate_entry(self):
        menu = Menu.objects.add_root(title="Menu1")
        e1 = Menu.objects.add_child(
            parent=menu,
            slug="l1",
            title="l1",
            content_object=Link.objects.create(url="#1")
        )
        e2 = Menu.objects.add_child(
            parent=menu,
            slug="l2",
            title="l2",
            content_object=Link.objects.create(url="#2")
        )
        data = menu.__dict__
        data['entry-text-0'] = "a"
        data['entry-text-1'] = "a"
        mf = MenuChangeForm(data, instance=menu)
        self.assertFalse(mf.is_valid())

        data['entry-text-1'] = "b"
        mf = MenuChangeForm(data, instance=menu)
        self.assertTrue(mf.is_valid())
