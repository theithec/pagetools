from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.fields import SlugField

from pagetools import search
from pagetools.core.models import PagelikeModel
from pagetools.pages.models import Page


class News(PagelikeModel):
    content = models.TextField()

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'News'

search.search_mods = (
   (Page, ('title', 'content')),
   (News, ('title', 'content')),
   #( app.models.Model2, ('foo','bar') ),
)


