
'''
Created on 15.12.2013

@author: Tim Heithecker
'''
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve

from django.contrib import admin

from django.test.testcases import TestCase

from pagetools.core.utils import get_adminedit_url, get_adminadd_url
from pagetools.widgets.models import (TypeArea, PageType)


class TypeAreaAdminTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'q@w.de', 'password')
        self.client.login(username="admin", password='password')
        self.site=admin.sites.AdminSite()
        self.pagetype= PageType.objects.create(name="base")
        #self.typearea = TypeArea.objects.create(
        #    type=self.pagetype, area="sidebar")

    def _test_add(self):
        response = self.client.post(
            get_adminadd_url(TypeArea),
            {
                #'type_id': self.pagetype.pk,
                'pagetype': self.pagetype.pk,
                'area': "sidebar",
                'widgets-TOTAL_FORMS':1,
                'widgets-INITIAL_FORMS':0,
                'save': True
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_edit(self):
        self._test_add()
        typearea = TypeArea.objects.get(
            pagetype=self.pagetype, area="sidebar")
        response = self.client.get(get_adminedit_url(typearea))
        self.assertEqual(response.status_code, 200)
