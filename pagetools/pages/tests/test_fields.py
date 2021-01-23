from django import forms
from django.test import TestCase

from pagetools.pages.forms import DynMultipleChoiceField, ValidationError


class TestForm(forms.Form):
    dmcf = DynMultipleChoiceField(label="dmcf: 1,2,3")


class FormsTestCase(TestCase):
    def test_valid_dyn_field(self):
        form = TestForm({"dmcf": ["1", "2"]})
        self.assertTrue(form.is_valid())

    def test_invalid_dyn_field(self):
        self.assertRaises(ValidationError, lambda: DynMultipleChoiceField(label="sowrong"))
