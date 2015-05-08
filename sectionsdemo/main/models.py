from django.db import models
from django.utils.translation import ugettext_lazy as _

from pagetools.sections.models import BasePageNode, BasePageNodePos, BasePageNodeManager


class PageNodeManager(BasePageNodeManager):
    #model = PageNode
    pass

class PageNode(BasePageNode):
    headline = models.CharField('Headline',  max_length=512, blank=True)
    text = models.TextField(blank=True)
    allowed_children_keys = ()
    objects = PageNodeManager()

    def save(self, *args, **kwargs):
        super(PageNode, self).save(*args, **kwargs)


class PageNodePos(BasePageNodePos):
    content = models.ForeignKey(PageNode)
    owner  = models.ForeignKey(PageNode, related_name="in_group")



class Section(PageNode):
    #allowed_children_classes = ('Row',)
    allowed_children_classes = ()

    class Meta:
        proxy = True
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')



class Page(PageNode):
    allowed_children_classes = (Section,)
    objects = PageNodeManager()

    class Meta:
        proxy = True
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
