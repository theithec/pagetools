from django.test import TestCase

from pagetools.widgets.context_processors import base_pagetype


class BasePageTypeTest(TestCase):

    def test_base(self):
        b = base_pagetype()
        self.assertIn("areas", b.keys())
