from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from demo_sections.tests import SectionsDataTestCase
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
                        'slug': self.articles[0].slug,
                    }), HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)


class Views2Test(MenuDataTestCase):

    def test_questionlist(self):
        qv = ViewLink.objects.create(name="polls:index")
        self.menu.children.add_child(
            parent=self.menu,
            content_object=qv,
            title="Polls",
            enabled=True
        )
        response = self.client.get(
            reverse("polls:index"))

        self.assertEqual(response.status_code, 200)



