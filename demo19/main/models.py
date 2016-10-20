from django.db import models
from django.core.urlresolvers import reverse
from filebrowser.fields import FileBrowseField

from pagetools.sections.models import TypeMixin, PageNode, PageNodeManager


class Article(PageNode):
    content = models.TextField("Content")
    teaser = models.TextField("Teaser")
    image = FileBrowseField("Image",max_length=200)
    allowed_children_classes = ["main.models.Article",]
    objects = PageNodeManager()

    def get_absolute_url(self):
        return reverse("main:article", kwargs={'slug': self.slug,})


class Section(TypeMixin, PageNode):
    node_choices = (
        ('section_style1', 'Style 1'),
        ('section_style2', 'Style 2'),
    )
    headline = models.CharField("Headline", max_length=255)
    allowed_children_classes = [Article,]
    objects = PageNodeManager()


class SectionList(PageNode):
    allowed_children_classes = [Section,]
    objects = PageNodeManager()
