'''
Created on 04.09.2012

@author: lotek
'''
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from pagetools.widgets.models import TemplateTagWidget

from pagetools.widgets.settings import TEMPLATETAG_WIDGETS


class Command(BaseCommand):
    # args = 'test: create test-mail'
    help = _('create Widgets according to settings.(PT_)TEMPLATETAG_WIDGETS ')

    def handle(self, *args, **options):
        for k, v in list(TEMPLATETAG_WIDGETS.items()):
            ttw = TemplateTagWidget.objects.create(
                name=k,
                renderclasskey=k,
            )
            print(("created: %s" % ttw))
