'''
Created on 14.12.2013

@author: lotek
'''

from django.test import TestCase

from pagetools.widgets.models import TypeArea, PageType, ContentWidget, \
    WidgetInArea
from django.contrib.contenttypes.models import ContentType


class WidgetTests(TestCase):

    def setUp(self):
        self.type1 = PageType.objects.get_or_create(name='base')[0]
        self.typearea1 = TypeArea.objects.get_or_create(
            area='sidebar',
            type=self.type1)[0]

    def test_model_creation(self):
        w1 = ContentWidget.objects.get_or_create(
            name='w1', content='foo')[0]
        co = ContentType.objects.get_for_model(w1)
        WidgetInArea.objects.get_or_create(
            typearea=self.typearea1,
            content_type=co,
            object_id=w1.pk,
            position=1)
        self.assertEqual(self.typearea1.widgets.all()[0].content_object, w1)

    def test_lists(self):
        self.assertEqual(self.typearea1.type, self.type1)
