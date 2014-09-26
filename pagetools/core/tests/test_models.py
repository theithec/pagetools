from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth.models import User
from django.db import models
from django.test.client import Client
from django.test.testcases import TestCase
from django.views.generic.detail import DetailView

from demo.project.urls import urlpatterns


settings.DEBUG = True

class Dummy(models.Model):
    slug = models.SlugField()
    status = models.TextField(max_length=10)

    def get_absolute_url(self):
        return "/%s" % self.slug


class DummyView(DetailView):
    model = Dummy
v = DummyView.as_view()
urlpatterns += urlpatterns(
                           url('/(?P<slug>[-\w]+)/$', v),
                           )


class DummyTests(TestCase):

    def setUp(self):
        self.username = 'admin'
        self.email = 'test@test.com'
        self.password = 'test'
        self.admin = User.objects.create_superuser(self.username, self.email, self.password)
        self.admin.save()
        print (self.admin)
        self.page = Dummy.objects.get_or_create(slug="p1", status="published")[0]


    def test_status(self):
        self.assertEqual(self.page.status, 'published')
        c = Client()
        resp = c.get(self.page.get_absolute_url())
        print(resp.response)
        self.assertEqual(resp.status_code, 200)

        self.page.status = 'draft'


        login = self.client.login(username=self.username, password=self.password)
        from django.contrib import auth
        user = auth.get_user(self.client)
        print("LOGIN; %s"% login, user)
        #self.page = Page.objects.get_or_create(title='p1', slug="p1")[0]
        resp = c.get(self.page.get_absolute_url())
        self.assertEqual(resp.status_code, 200)