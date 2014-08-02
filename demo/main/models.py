from django.db import models
from pagetools import search
from pagetools.core.models import PagelikeModel
from pagetools.pages.models import Page
from django.db.models.fields import SlugField


class News(PagelikeModel):
    content = models.TextField()

    class Meta:
        verbose_name_plural = 'News'

search.search_mods = (
   (Page, ('title', 'content')),
   (News, ('title', 'content')),
   #( app.models.Model2, ('foo','bar') ),
)


