'''
Created on 14.12.2013

@author: lotek
'''

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from django.contrib import auth
from pagetools.core.settings import STATUS_PUBLISHED
from pagetools.pages.models import Page


class TC1Tests(TestCase):

    def setUp(self):
        self.username = 'admin'
        self.email = 'test@test.com'
        self.password = 'test'
        self.admin = User.objects.create_superuser(self.username, self.email, self.password)
        self.admin.save()
        self.page = Page.objects.get_or_create(title='p1', slug="p1")[0]

    def test_title(self):
        self.assertEqual(self.page.title, 'p1')

    def test_draft(self):
        self.assertEqual(self.page.status, 'draft')
        resp = self.client.get(self.page.get_absolute_url())
        self.assertEqual(resp.status_code, 404)

    def test_draft_admin(self):
        self.assertEqual(self.page.status, 'draft')
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.page.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_published(self):
        self.page.status = STATUS_PUBLISHED
        self.page.save()
        resp = self.client.get(self.page.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        self.client.logout()
