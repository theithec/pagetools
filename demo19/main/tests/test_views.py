from django.test import TestCase, RequestFactory
#from django import urls
from demo import urls
# from django.conf.urls import url, include
from main.tests import SectionsDataTestCase


class ViewsTest(SectionsDataTestCase):


    def test_view(self):
        response = self.client.get(self.sectionlist1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
