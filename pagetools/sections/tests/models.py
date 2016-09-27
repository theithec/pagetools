from django.db import models
from pagetools.sections.models import PageNode


class TSectionPage1(PageNode):
    foo = models.CharField("Foo", max_length=8)

