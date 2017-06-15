
'''
Created on 14.12.2013

@author: Tim Heithecker
'''
from django.db.models.base import ModelBase
from django.db import connection


from django.contrib.auth.models import User
from django.test import TestCase
from pagetools.core.settings import STATUS_PUBLISHED
from pagetools.sections.models import PageNode, TypeMixin
from django.db import models
from django.conf import settings

settings.IS_TEST = True




class TestModelMixin(TestCase):

    def setUp(self):

        from pagetools.sections.tests.models import PageNodeDummy
        self.model = PageNodeDummy
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(self.model)

        self.n1 = self.model.objects.create(title="w1")

    def tearDown(self):
        # Delete the schema for the test model
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(self.model)

class ModelTests(TestModelMixin):

    def test_title(self):
        self.assertEqual(self.n1.title, "w1")
