from django.test import TransactionTestCase

from pagetools.menus.models import Menu, Link, ViewLink
from pagetools.pages.models import Page
from pagetools.core.settings import STATUS_PUBLISHED
from pagetools.core.tests.test_models import ConcretePublishableLangModel


class MenuDataTestCase(TransactionTestCase):
    fixtures = ["testdata.json"]
    def setUp(self):
        k1 = {'status': STATUS_PUBLISHED}
        k2 = {'enabled': True}
        self.menu = Menu.objects.add_root(title='MainMenu')
        self.v1 = ViewLink.objects.create(name="index")
        self.e_v1 = Menu.objects.add_child(self.menu, self.v1, **k2)
        self.p1 = Page.objects.create(title='P1', slug='start', status=STATUS_PUBLISHED, included_form="Contactform")
        self.e_p1 = Menu.objects.add_child(self.menu, self.p1, **k2)
        self.l1 = Link.objects.create(url='#')
        self.e_l1 = Menu.objects.add_child(self.menu, self.l1, **k2)
        self.l2 = Link.objects.create(url='/foo')
        self.e_l2 = self.e_l1.children.add_child(self.menu, self.l2)
        self.c1 = ConcretePublishableLangModel.objects.create(
            foo="x", status=STATUS_PUBLISHED)
        self.e_c1 = Menu.objects.add_child(self.menu, self.c1, **k2)
        #  print("CL", self.menu.children , self.menu.children_list(for_admin=True), **k)


