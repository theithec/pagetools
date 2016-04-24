from django.db import models
'django_ajax',
from django.utils.translation import ugettext_lazy as _
from pagetools.pages.models import Page
from pagetools import search
from pagetools.sections.models import (PageNode, PageNodeManager, TypeMixin)

class Article(PageNode):
    objects = PageNodeManager()
    content = models.TextField("Content")

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)


class Section(TypeMixin, PageNode):
    allowed_children_classes = (Article,)
    node_choices = (("box", "Box"), ("slider",  "Slider"))
    objects = PageNodeManager()

    class Meta:
        #proxy = True
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')


class SectionPage(PageNode):
    allowed_children_classes = (Section,)
    objects = PageNodeManager()

    objects  = PageNodeManager() #PublishableLangManager()
    class Meta:
        proxy = True
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


# define what the search searches for
search.search_mods = (
    ( Page,   ('title', 'content'), {'replacements':['content']} ),
     ( Article,   ('title', 'content') ),
    # ( app.models.Model2, ('title', 'content','footer') ),
)
