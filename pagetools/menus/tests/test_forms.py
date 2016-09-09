from django.core import urlresolvers
from django.test.testcases import TestCase
from pagetools.menus.models import Menu, Link
from pagetools.menus.admin import MenuAddForm, MenuChangeForm


class MenuFormTests(TestCase):
    def test_menu_addform(self):
        mf = MenuAddForm({'title': 'Testmenu1'})
        self.assertTrue(mf.is_valid())

    def test_add_menu(self):
        menuaddurl = urlresolvers.reverse('admin:menus_menu_add', args=[])
        response = self.client.post(menuaddurl, {'title': 'Testmenu1'})
        self.assertTrue(response.status_code in (200, 302))

    def test_menuchildrenwidgets(self):
        menu = Menu.objects.add_root(title="Menu1")
        Menu.objects.add_child(
            parent=menu,
            slug="l1",
            title="l1",
            content_object=Link.objects.create(url="#1")
        )
        data = menu.__dict__
        mf = MenuChangeForm(data, instance=menu)
        self.assertTrue('value="l1"' in mf.as_p())

    def test_dublicate_entry(self):
        menu = Menu.objects.add_root(title="Menu1")
        Menu.objects.add_child(
            parent=menu,
            slug="l1",
            title="l1",
            content_object=Link.objects.create(url="#1")
        )
        Menu.objects.add_child(
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
