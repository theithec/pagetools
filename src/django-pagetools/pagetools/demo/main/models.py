from django.db import models
from pagetools.models import  PublishableModel, LangModel
from model_utils.models import StatusModel


class News(PublishableModel, LangModel):
    title = models.CharField(max_length=128)
    content = models.TextField()
    
    class Meta:
        verbose_name_plural = 'News'
    

import pagetools
from pagetools import pages
pagetools.search.search_mods = (
   (pages.models.Page, ('title', 'content')),
  # ( app.models.Model2, ('foo','bar') ),
)


