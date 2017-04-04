from django import forms
from django.test import TestCase

from pagetools.pages.forms import *


class TestForm(forms.Form):
    dmcf = DynMultipleChoiceField(label="dmcf: 1,2,3")


class FormsTestCase(TestCase):
    def test_valid_DMCF(self):
        f = TestForm({
            'dmcf': ["1", "2"]
        })
        v = f.is_valid()
        # print(vars(f))
        self.assertTrue(v)

    def test_invalid_DMCF(self):
        self.assertRaises(
            ValidationError,
            lambda: DynMultipleChoiceField(label="sowrong"))
