'''
Created on 04.09.2012

@author: lotek
'''
from django.core.management.base import BaseCommand

from pagetools.widgets.models import TemplateTagWidget

from pagetools.widgets.settings import TEMPLATETAG_WIDGETS
class Command(BaseCommand):
    # args = 'test: create test-mail'
    help = u'create Widgets according to settings.(PT_)TEMPLATETAG_WIDGETS '

    def handle(self, *args, **options):
        for k, v in TEMPLATETAG_WIDGETS.items():
            ttw = TemplateTagWidget.objects.create(
                name=k,
                renderclasskey=k,
            )
            print u"created: %s" % ttw
