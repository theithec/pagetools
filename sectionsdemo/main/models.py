from django.db import models
'django_ajax',
from django.utils.translation import ugettext_lazy as _

from pagetools.sections.models import (PageNode,
                                       PageNodePos, PageNodeManager, TypeMixin)

class Article(PageNode):
    objects  = PageNodeManager() #PublishableLangManager()
    content = models.TextField("Content")

    def __init__(self,*args,**kwargs):
        #kwargs['allowed_children_keys'] = (self.__class__,)
        self.allowed_children_classes = (self.__class__,)
        super(Article, self).__init__(*args, **kwargs)

class Section(TypeMixin, PageNode):
    allowed_children_classes = (Article,)
    node_choices = (("box", "Box"),("slider",  "Slider")) 
    objects  = PageNodeManager() #PublishableLangManager()
    class Meta:
        #proxy = True
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')



class Page(PageNode):
    allowed_children_classes = (Section,)
    objects = PageNodeManager()

    objects  = PageNodeManager() #PublishableLangManager()
    class Meta:
        proxy = True
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
