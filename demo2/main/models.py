from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from pagetools.core.models import PagelikeModel
from pagetools.subscribe.utils import to_queue

def blog_save_callback(sender, **kwargs):
    obj = kwargs['instance']
    to_queue({'title':obj.title, 'body': obj.content})

class BlogEntry(PagelikeModel):
    content = models.TextField()

post_save.connect(blog_save_callback, sender=BlogEntry)
