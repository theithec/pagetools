from django.contrib.admin import AdminSite
from django.db.models.base import ModelBase

from django.test import TestCase
from django.db import models
from pagetools.sections.dashboard_modules import PageNodesModule
import pagetools.sections.dashboard_modules

from pagetools.sections.models import PageNode
from pagetools.sections.admin import BasePageNodeAdmin
from pagetools.sections.tests.test_models import TestModelMixin


class MockRequest(object):
    pass


request = MockRequest()


class SectionAdminTests(TestModelMixin):

    def setUp(self):
        super().setUp()

        self.site = AdminSite()

    def test_foo1(self):
        ma = BasePageNodeAdmin(PageNode, self.site)
        self.assertEqual(list(ma.get_fields(request)), [
            'status', 'lang', 'title', 'slug', 'description',
            'classes', 'content_type_pk', 'status_changed',
            'containing_nodes'])
