from unittest.mock import Mock

from django.contrib.admin import AdminSite

from pagetools.sections.models import PageNode
from pagetools.sections.admin import BasePageNodeAdmin
from pagetools.sections.tests.test_models import TestModelMixin


class SectionAdminTests(TestModelMixin):
    def setUp(self):
        super().setUp()

        self.site = AdminSite()

    def test_has_fields(self):
        admin = BasePageNodeAdmin(PageNode, self.site)
        self.assertEqual(
            list(admin.get_fields(Mock())),
            [
                "status",
                "lang",
                "title",
                "slug",
                "description",
                "classes",
                "content_type_pk",
                "status_changed",
                "containing_nodes",
            ],
        )
