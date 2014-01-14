'''
Created on 14.12.2013

@author: lotek
'''

from django.test import TestCase

from pagetools.widgets.models import TypeArea, PageType, ContentWidget, \
    WidgetInArea


class TCTests(TestCase):

    def setUp(self):
        self.type1 = PageType.objects.get_or_create(name='base')[0]
        self.typearea1 = TypeArea.objects.get_or_create(
            area='sidebar',
            type=self.type1)[0]
        self.w1 = ContentWidget.objects.get_or_create(
                                name='w1', content=u'foo')[0]
        WidgetInArea.objects.get_or_create(
            typearea=self.typearea1,
            widget=self.w1.adapter.all()[0],
            position=1)

    def test_lists(self):
        self.assertEqual(self.typearea1.type, self.type1)
        self.assertEqual(self.typearea1.widgets.all()[0].content_object, self.w1)
