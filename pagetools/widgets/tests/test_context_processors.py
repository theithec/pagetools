from unittest import mock
from django.test import TestCase

from pagetools.widgets.context_processors import base_pagetype


class BasePageTypeTest(TestCase):
    def test_base(self):
        request = mock.MagicMock()
        request.areas_added = False
        request.META = {}
        b = base_pagetype(request)
        self.assertIn("areas", b.keys())
