from django.db import models
from django.utils.translation import ugettext_lazy as _
from filebrowser.fields import FileBrowseField
from pagetools.core.models import  PublishableLangModel, PublishableLangManager

class BasePageNode(PublishableLangModel):

    group_choices = (
        ('page', 'Page'),
        ('section', 'Section'),
        ('content', 'Content'),
        ('product', 'Product'),
        ('product-landing', 'Product-Landing'),
        ('round-icons', 'Round Icons Row'),
        ('angular-icons', 'Angular Icons Row'),
        ('slider', 'Slider'),
        # ('text', 'Text'),
        # ('image', 'Image'),
        # ('video', 'Movie'),
    )
    title  = models.CharField(_('Internal Title'), max_length=512)
    image = FileBrowseField(_('Image'), max_length=250,blank=True, extensions=[".jpg", ".gif", ".png"])
    video_m4v = FileBrowseField(_('Video: m4v'), max_length=250,blank=True, extensions=[".m4v"])
    video_ogv = FileBrowseField(_('Video: ogv'), max_length=250,blank=True, extensions=[".ogv"])
    video_webm = FileBrowseField(_('Video: webm'), max_length=250,blank=True, extensions=[".webm"])
    video_poster = FileBrowseField(_('Video: Poster'), max_length=250,blank=True, extensions=[".jpg",".jpeg", ".gif", ".png"])
    slug = models.SlugField(_('Slug'), max_length=128)
    target = models.ForeignKey("self", blank=True, null=True)
    classes = models.CharField(max_length=512, blank=True, null=True)
    node_type = models.CharField(max_length=128, choices=group_choices)



    in_nodes = models.ManyToManyField("self",
                                      through="PageNodePos",
                                      related_name="positioned_content",
                                      symmetrical=False)

    objects  = PublishableLangManager()

    def _videofield(self, type):
        return  getattr(self, 'video_%s' % type)

    def videofiles(self):
        v = "<br />".join(
            ['%s: %s' %(v, self._videofield(v))
                for v in "m4v ogv webm poster".split()
                if self._videofield(v)
            ]
        )
        return v
    videofiles.allow_tags=True

    def with_long_slug(self, content):
        s =  self.slug + "_" + content.slug
        content.long_slug = s
        return content

    def ordered_content(self, **kwargs):
        user = kwargs.pop('user', None)
        #if not user or not user.is_authenticated():
        #    kwargs['status'] = ptsettings.STATUS_PUBLISHED
        #o = self.positioned_content.language().fallbacks('en').filter(**kwargs).order_by('in_group__position')
        o = self.positioned_content.lfilter(**kwargs).order_by('in_group__position')
        return [self.with_long_slug(c) for c in o]

    def __str__(self):
        return "[%s]:%s(%s)" % (self.node_type, self.title, self.lang or "all")
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
