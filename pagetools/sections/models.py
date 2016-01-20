from django.db import models, DatabaseError
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from pagetools.core.models import PagelikeModel, PublishableLangManager
from pagetools.core.utils import get_adminadd_url


class PageNodeManager(PublishableLangManager):
    pass


class TypeMixin(models.Model):

    node_choices = ()
    node_type = models.CharField(max_length=128, blank=True)

    def __init__(self, *args, **kwargs):
        super(TypeMixin, self).__init__(*args, **kwargs)
        self._meta.get_field('node_type')._choices = self.node_choices

    class Meta:
        abstract = True


class PageNode(PagelikeModel):

    classes = models.CharField('Classes', max_length=512, blank=True, null=True)
    content_type_pk = models.SmallIntegerField(blank=True)
    in_nodes = models.ManyToManyField("self",
                                      through="PageNodePos",
                                      related_name="positioned_content",
                                      symmetrical=False)
    objects = PageNodeManager()
    @classmethod
    def get_adminadd_url(Clz):
        return get_adminadd_url(Clz)

    @classmethod
    def get_classname(Clz):
        return Clz._meta.verbose_name

    def get_real_obj(self, node=None):
        node = node or self
        #import pdb; pdb.set_trace()

        clz = ContentType.objects.get_for_id(node.content_type_pk)
        real = clz.model_class().objects.get(pk=node.pk)
        #print("Node", node.title,  node.content_type_pk, clz, real.get_classname())
        try:
            clz = ContentType.objects.get_for_id(node.content_type_pk)
            real = clz.model_class().objects.get(pk=node.pk)
        except AttributeError as e:
            real = node
        return real

    def get_real_content(self, _content):
        content = self.get_real_obj(_content)
        s =  self.slug + "_" + content.slug
        content.long_slug = s
        return content

    def ordered_content(self, **kwargs):
        #import pdb; pdb.set_trace()
        o = self.positioned_content.lfilter(**kwargs).order_by('pagenodepos')
        return [self.get_real_content(c) for c in o]

    def __str__(self):
        o = self.get_real_obj()
        return "%s(%s)" % (o.title ,o.get_classname())

    def save(self, *args, **kwargs):
        if not self.content_type_pk:
            ct = ContentType.objects.get_for_model(self, for_concrete_model=False)
            self.content_type_pk = ct.pk
        super(PageNode, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/#%s" % self.slug

    @classmethod
    def get_contenttype_pk(cls):
        t = ContentType.objects.get_for_model(cls, for_concrete_model=False)
        return t.id

    class Meta:
        verbose_name = _('Node')
        verbose_name_plural = _('Nodes')


class PageNodePos(models.Model):

    position = models.PositiveIntegerField()
    content = models.ForeignKey(PageNode)
    owner  = models.ForeignKey(PageNode, related_name="in_group")

    def __str__(self):
        return "%s:%s:%s" %(self.owner, self.content, self.position)

    class Meta:
        ordering = ['position']
        verbose_name = _('Content Position')
        verbose_name_plural = _('Content Positions')

