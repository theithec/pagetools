from django.db import models
from pagetools import search
from pagetools.core.models import PublishableModel, LangModel
from pagetools.pages.models import Page


class News(PublishableModel, LangModel):
    title = models.CharField(max_length=128)
    content = models.TextField()

    class Meta:
        verbose_name_plural = 'News'

search.search_mods = (
   (Page, ('title', 'content')),
   #( app.models.Model2, ('foo','bar') ),
)


