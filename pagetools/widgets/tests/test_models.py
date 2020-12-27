from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from pagetools.widgets.models import ContentWidget, PageType, TypeArea, WidgetInArea


class WidgetTests(TestCase):
    def setUp(self):
        self.type1 = PageType.objects.get_or_create(name="base")[0]
        self.typearea1 = TypeArea.objects.get_or_create(
            area="sidebar", pagetype=self.type1
        )[0]

    def test_model_creation(self):
        widget = ContentWidget.objects.get_or_create(name="w1", content="foo")[0]
        ctype = ContentType.objects.get_for_model(widget)
        WidgetInArea.objects.get_or_create(
            typearea=self.typearea1, content_type=ctype, object_id=widget.pk, position=1
        )
        self.assertEqual(self.typearea1.widgets.all()[0].content_object, widget)

    def test_lists(self):
        self.assertEqual(self.typearea1.pagetype, self.type1)
