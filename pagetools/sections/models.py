from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from filebrowser.fields import FileBrowseField
from pagetools.core.models import  PublishableLangModel, PublishableLangManager
#from .settings import AVAIL_NODES



class BasePageNodeManager(PublishableLangManager):
    def get_queryset(self):
        #print ("MANA", self.__dict__)
        ct = ContentType.objects.get_for_model(self.model, for_concrete_model=False)
        print ("MANA2", self.model, ct)
        return super(BasePageNodeManager, self).get_queryset().filter(content_type_pk=ct.id)

class BasePageNode(PublishableLangModel):

    title  = models.CharField(_('Internal Title'), max_length=512)
    #image = FileBrowseField(_('Image'), max_length=250,blank=True, extensions=[".jpg", ".gif", ".png"])
    #video_m4v = FileBrowseField(_('Video: m4v'), max_length=250,blank=True, extensions=[".m4v"])
    #video_ogv = FileBrowseField(_('Video: ogv'), max_length=250,blank=True, extensions=[".ogv"])
    #video_webm = FileBrowseField(_('Video: webm'), max_length=250,blank=True, extensions=[".webm"])
    #video_poster = FileBrowseField(_('Video: Poster'), max_length=250,blank=True, extensions=[".jpg",".jpeg", ".gif", ".png"])
    slug = models.SlugField(_('Slug'), max_length=128)
    #target = models.ForeignKey("self", blank=True, null=True)
    #classes = models.CharField(max_length=512, blank=True, null=True)
    #    node_type = models.CharField(max_length=128, choices=AVAIL_NODES)


    content_type_pk = models.SmallIntegerField(blank=True)
    in_nodes = models.ManyToManyField("self",
                                      through="PageNodePos",
                                      related_name="positioned_content",
                                      symmetrical=False)

    #ct = ContentType.objects.get_for_model(self, for_concrete_model=False)
    #self.content_type_pk = ct.pk
    #objects  = BasePageNodeManager() #PublishableLangManager()

    #def _videofield(self, type):
    #    return  getattr(self, 'video_%s' % type)

    #def videofiles(self):
    #    v = "<br />".join(
    #        ['%s: %s' %(v, self._videofield(v))
    #            for v in "m4v ogv webm poster".split()
    #            if self._videofield(v)
    #        ]
    #    )
    #    return v
    #videofiles.allow_tags=True

    def get_real_obj(self, node):
        clz = ContentType.objects.get_for_id(node.content_type_pk)
        return clz.model_class().objects.get(pk=node.pk)

    def get_real_content(self, _content):
        content = self.get_real_obj(_content)
        print ("CC", _content.__class__)
        s =  self.slug + "_" + content.slug
        content.long_slug = s
        #print "CONTEN"
        return content

    def ordered_content(self, **kwargs):
        #user = kwargs.pop('user', None)
        #if not user or not user.is_authenticated():
        #    kwargs['status'] = ptsettings.STATUS_PUBLISHED
        #o = self.positioned_content.language().fallbacks('en').filter(**kwargs).order_by('in_group__position')
        print("SELF", self)
        o = self.positioned_content.lfilter(**kwargs).order_by('in_group__position')
        return [self.get_real_content(c) for c in o]

    def __str__(self):
        return self.title
        return "[%s]:%s %s)" % (self.node_type, self.title, self.lang or "")


    def save(self, *args, **kwargs):
        #print("save",self._meta.object_name,   self._meta,"\n".join([("%s\t%s" % (k,v)) for k,v in self._meta.__dict__.items()]) , args, kwargs)
        if not self.content_type_pk:
            ct = ContentType.objects.get_for_model(self, for_concrete_model=False)
            self.content_type_pk = ct.pk
            print ("CT", ct, ct.pk, self._meta.concrete_model)
        super(BasePageNode, self).save(*args, **kwargs)

    @classmethod
    def get_contenttype_pk(cls):
        t = ContentType.objects.get_for_model(cls, for_concrete_model=False)
        return t.id

    class Meta:
        abstract = True
        verbose_name = _('Node')
        verbose_name_plural = _('Nodes')




class BasePageNodePos(models.Model):
    position = models.PositiveIntegerField()

    def __str__(self):
        return "%s:%s:%s" %(self.owner, self.content, self.position)

    class Meta:
        abstract = True
        ordering = ['position']
        verbose_name = _('Content Position')
        verbose_name_plural = _('Content Positions')


class PageNode(BasePageNode):
    headline = models.CharField('Headline',  max_length=512, blank=True)
    text = models.TextField(blank=True)
    allowed_children_keys = ()
    #objects = PageNodeManager()

    def save(self, *args, **kwargs):
        super(PageNode, self).save(*args, **kwargs)


class PageNodePos(BasePageNodePos):
    content = models.ForeignKey(PageNode)
    owner  = models.ForeignKey(PageNode, related_name="in_group")




