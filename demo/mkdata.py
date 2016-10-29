import os, sys # noqa
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'
django.setup()

#  from django.conf import settings
from django.core import management  #noqa
from django.utils import timezone #noqa
from django.contrib.auth.models import User #noqa

from pagetools.core.settings import STATUS_PUBLISHED #noqa
from pagetools.menus.models import Menu, AutoPopulated, ViewLink #noqa
from pagetools.pages.models import Page #noqa
from pagetools.widgets.models import (PageType,  TypeArea, ContentWidget, # noqa
                                      WidgetInArea, TemplateTagWidget) #noqa
import pagetools.menus.utils #noqa
from polls.models import Question, Choice #noqa

management.call_command("migrate")
try:
    User.objects.create_superuser("admin", "q@w.de", "pass#word")
except:
    sys.exit("Error. DB exists?")

import _data
_data.create()


