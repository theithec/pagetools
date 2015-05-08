from django.db import models
from django.utils.translation import ugettext_lazy as _

from pagetools.sections.models import PageNode, BasePageNodePos, BasePageNodeManager



class Section(PageNode):
    #allowed_children_classes = ('Row',)
    allowed_children_classes = ()

    objects  = BasePageNodeManager() #PublishableLangManager()
    class Meta:
        proxy = True
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')



class Page(PageNode):
    allowed_children_classes = (Section,)
    objects = BasePageNodeManager()

    objects  = BasePageNodeManager() #PublishableLangManager()
    class Meta:
        proxy = True
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
