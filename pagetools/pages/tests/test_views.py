'''
Created on 15.12.2013

@author: Tim Heithecker
'''

from pagetools.menus.tests import MenuDataTestCase


class PageViewTestCase(MenuDataTestCase):

    def test_indexview(self):
        response = self.client.get(self.v1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
