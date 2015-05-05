from django.db import models
from django.utils.translation import ugettext_lazy as _
from filebrowser.fields import FileBrowseField
from pagetools.core.models import  PublishableLangModel
from pagetools.core import settings as ptsettings


class BaseNode(PublishableLangModel):
    group_choices = (
        ('page', 'Page'),
        ('section', 'Section'),
        ('content', 'Content'),
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
    contents = models.ManyToManyField("self", through="NodePos",
                                       related_name="positioned_content", symmetrical=False)
    # translations = TranslatedFields(
    #    headline = models.CharField('Headline',  max_length=512, blank=True),
    #    text = models.TextField(blank=True),
    #)
    allowed_children_keys = ()
    #object = PubTransManager()

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
        if not user or not user.is_authenticated():
            kwargs['status'] = ptsettings.STATUS_PUBLISHED
        o = self.positioned_content.language().fallbacks('en').filter(**kwargs).order_by('in_group__position')
        return [self.with_long_slug(c) for c in o]

    def __str__(self):
        return "[%s]:%s(%s)" % (self.node_type, self.title, self.lang or "all")

    class Meta:
        abstract = True
        verbose_name = _('Node')
        verbose_name_plural = _('Nodes')
        unique_together = (("slug", "node_type", "lang"),)


class BaseNodePos(models.Model):
    position = models.PositiveIntegerField()

    def __str__(self):
        return "%s:%s:%s" %(self.group, self.content, self.position)

    class Meta:
        abstract = True
        ordering = ['position']
        verbose_name = _('Content Position')
        verbose_name_plural = _('Content Positions')
