from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from main.tests import SectionsDataTestCase
from polls.views import IndexView
from pagetools.menus.tests import MenuDataTestCase
from pagetools.menus.models import ViewLink


class Views1Test(SectionsDataTestCase):


    def test_view(self):
        response = self.client.get(self.sectionlist1.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_ajaxview(self):
        response = self.client.get(
            reverse("sections:ajax",
                    kwargs={
                        'slug': self.sectionlist1.slug,
                    }), HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)


class Views2Test(MenuDataTestCase):

    def test_questionlist(self):
        qv = ViewLink.objects.create(name="polls:index")
        self.menu.children.add_child(
            parent=self.menu,
            content_object=qv,
            title="Polls234",
            enabled=True
        )
        print ("\n\nMC", self.menu.children_list(for_admin=True))
        response = self.client.get(
            reverse("polls:index"))
        print("r2", response.content)

        self.assertEqual(response.status_code, 200)



