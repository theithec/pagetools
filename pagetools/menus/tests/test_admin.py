'''
Created on 15.12.2013

@author: lotek
'''
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.test.testcases import TestCase


class MenuAdminTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'q@w.de', 'password')


    def test_admin_index(self):  # customdashboard with MenuModule not broken
        self.client.login(username="admin", password='password')
        adminindex = urlresolvers.reverse('admin:index', args=[])
        response = self.client.get(adminindex, {})
        self.assertTrue(response.status_code in (200, 302))
