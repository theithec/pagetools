'''
import django
from selenium import webdriver
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class SeleniumTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Firefox()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'q@w.de', 'password')
        self.client.login(username="admin", password='password')
        super().setUp()
'''
