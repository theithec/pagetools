'''
Created on 15.12.2013

@author: Tim Heithecker
'''
from django.contrib.auth.models import User
from django.core import urlresolvers

from django.contrib import admin

from django.test.testcases import TestCase
from pagetools.menus.models import Menu, MenuEntry, Link
from pagetools.menus.admin import MenuAdmin, make_entrieable_admin
from pagetools.menus import _ENTRIEABLE_MODELS
from pagetools.core.tests.test_models import ConcretePublishableLangModel
from pagetools.sections.tests.test_models import TestNode1
from pagetools.sections.dashboard_modules import PageNodesModule
from pagetools.core.utils import get_adminedit_url


class CPMAdmin(admin.ModelAdmin):
    model = ConcretePublishableLangModel


admin.site.register(ConcretePublishableLangModel, CPMAdmin)


PageNodesModule.model = TestNode1


class MenuAdminTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'admin', 'q@w.de', 'password')
        self.client.login(username="admin", password='password')
        self.site = admin.site

    def test_admin_index(self):
        ''' test index because customdashboard with MenuModule is may used'''
        adminindex = urlresolvers.reverse('admin:index')
        response = self.client.get(
            adminindex, follow=True, extra={'app_label': "admin"})
        self.assertIn(response.status_code, (200, 302))

    def test_add(self):
        adminurl = urlresolvers.reverse('admin:menus_menu_add', args=[])
        self.client.post(adminurl, {'title': 'Menu1'})
        m = Menu.objects.get(title="Menu1")
        self.assertEqual(len(m.children.all()), 0)
        return m

    def test_update(self):
        m = Menu.objects.add_root(title="Menu1")
        e = []
        for i in range(1, 3):
            e.append(
                MenuEntry.objects.add_child(
                    parent=m, title="e%s" % i,
                    content_object=Link.objects.create(url='#%s' % i,),
                    enabled=True
                )
            )
        adminurl = urlresolvers.reverse('admin:menus_menu_change', args=[m.pk])
        response = self.client.get(adminurl, {'pk': m.pk})
        data = m.__dict__
        data['entry-order-id-0'] = e[0].pk
        data['entry-text-0'] = "changed"
        data['entry-published-0'] = 1
        response = self.client.post(adminurl, data)
        cl = m.children_list()
        self.assertEqual(cl[0]['entry_title'], "changed")

    def test_reorder(self):
        m = Menu.objects.add_root(title="Menu1")
        e = []
        for i in range(1, 3):
            e.append(
                MenuEntry.objects.add_child(
                    parent=m, title="e%s" % i,
                    content_object=Link.objects.create(url='#%s' % i,),
                    enabled=True
                )
            )

        adminurl = urlresolvers.reverse('admin:menus_menu_change', args=[m.pk])
        data = m.__dict__
        response = self.client.post(adminurl, data)
        self.assertEqual([e['entry_title'] for e in m.children_list()],
                         ['e1', 'e2'])
        data.update({
            'entry-order': "[%s]=null&[%s]=null" % (e[1].pk, e[0].pk),
        })
        response = self.client.post(adminurl, data)
        self.assertEqual([e['entry_title'] for e in m.children_list()],
                         ['e2', 'e1'])

    def test_addentry(self):
                m = Menu.objects.add_root(title="Menu1", enabled=True)
                e = []
                for i in range(1, 3):
                    e.append(
                        MenuEntry.objects.add_child(
                            parent=m, title="e%s" % i,
                            content_object=Link.objects.create(url='#%s' % i,),
                            enabled=True
                        )
                    )
                    adminurl = urlresolvers.reverse(
                        'admin:menus_menu_change', args=[m.pk])
                    data = m.__dict__
                    data['addentry'] = 'menus#link'

                response = self.client.post(adminurl, data)

    def test_addableentries(self):
        ma = MenuAdmin(model=Menu, admin_site=self.site)

        m = Menu.objects.add_root(title="Menu1")
        e = ma.addable_entries(obj=m)
        for m in _ENTRIEABLE_MODELS:
            self.assertEqual(e.count('<li>'), len(_ENTRIEABLE_MODELS))

    def test_mk_entriableadmin(self):
        CA = CPMAdmin
        make_entrieable_admin(CA)
        self.assertTrue(CA.is_menu_entrieable)

        ca = CA(model=ConcretePublishableLangModel, admin_site=self.site)
        c = ConcretePublishableLangModel.objects.create(foo="x")
        m = Menu.objects.add_root(title="Menu1")
        self.assertTrue(ca.get_fields({}, c), [])
        self.assertTrue(ca.get_fieldsets({}, c), [])
        F = CA.form
        F._meta.model = ConcretePublishableLangModel
        f = F(c.__dict__)
        self.assertTrue('menus' in f.fields.keys())
        v = f.is_valid()
        self.assertTrue(v)

        data = c.__dict__
        data['menus'] = [m.pk]
        f = F(data, instance=c)
        self.assertTrue('menus' in f.fields.keys())
        v = f.is_valid()
        self.assertTrue(v)

        adminurl = get_adminedit_url(c)
        data = c.__dict__
        data['status_changed_0'] = "2016-01-01"
        data['status_changed_1'] = "23:00"
        # import pdb; pdb.set_trace()
        response = self.client.post(adminurl, data)
        self.assertIn(response.status_code, (200, 302))
