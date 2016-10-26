from django.core.management import call_command
from django.test import TestCase

from pagetools.widgets.settings import TEMPLATETAG_WIDGETS
from pagetools.widgets.models import *

class CommandsTestCase(TestCase):
    def test_mycommand(self):
        " Test my custom command."

        args = []
        opts = {}
        call_command('mk_templatetagwidgets', *args, **opts)
        tw = TemplateTagWidget.objects.all()
        self.assertEqual(len(TEMPLATETAG_WIDGETS), len(tw))
