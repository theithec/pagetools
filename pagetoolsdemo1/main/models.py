from django.db import models
from pagetools.pages.models import Page
from pagetools import search

# Create your models here.
search.search_mods = (
     ( Page,   ('title', 'content') ),
    # ( app.models.Model2, ('title', 'content','footer') ),
)
