from django.contrib.admin import AdminSite

from django.test import TestCase
from django.db import models
from pagetools.sections.dashboard_modules import PageNodesModule

from pagetools.sections.models import PageNode
from pagetools.sections.admin import BasePageNodeAdmin

from pagetools.sections.tests.test_models import TestNode1

PageNodesModule.model = TestNode1
class MockRequest(object):
    pass


request = MockRequest()


class SectionAdminTests(TestCase):

    def setUp(self):
        self.site = AdminSite()

    def test_foo1(self):
        ma = BasePageNodeAdmin(PageNode, self.site)
        self.assertEqual(list(ma.get_fields(request)), [
            'status', 'lang',  'title', 'slug',  'description',
            'classes', 'content_type_pk', 'status_changed',
            'containing_nodes'])
