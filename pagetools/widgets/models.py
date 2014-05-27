'''
Created on 14.12.2013

@author: lotek
'''

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.context import Context
from django.utils import importlib
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from pagetools.core.models import LangModel, LangManager

from . import settings


class WidgetAdapter(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u'%s' % self.content_object

    def get_title(self):
        return u'%s' % self.content_object.title

    def get_content(self, contextdict):
        return self.content_object.get_content(contextdict)


class BaseWidget(models.Model):
    title = models.CharField(max_length=128, blank=True)
    name = models.SlugField(_('Internal Name'), unique=True)
    adapter = generic.GenericRelation('WidgetAdapter')

    def save(self, *args, **kwargs):
        super(BaseWidget, self).save(*args, **kwargs)
        WidgetAdapter.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk
        )

    def __unicode__(self):
        return u"%s" % self.title or self.name

    class Meta:
        abstract = True


class ContentWidget(BaseWidget):
    content = models.TextField(_('Content'))

    def get_title(self):
        return self.title or self.name

    def get_content(self, contextdict):
        return self.content


class TemplateTagWidget(BaseWidget):
    renderclasskey = models.CharField(
        max_length=255,
        choices=[(k, k) for k in settings.TEMPLATETAG_WIDGETS.keys()]
    )

    def __init__(self, *args, **kwargs):
        super(TemplateTagWidget, self).__init__(*args, **kwargs)
        self.robj = None

    def get_rendererobject(self):
        if not self.robj:
            modulename, clsname = settings.TEMPLATETAG_WIDGETS.get(
                self.renderclasskey,
                (None, None)
            )
            module = importlib.import_module(modulename)
            try:
                self.robj = getattr(module, clsname)()
            except KeyError:
                pass
        return self.robj

    def get_title(self):
        return u'%s' % self.title

    def get_content(self, contextdict):
        if self.get_rendererobject():
            return self.robj.render(Context(contextdict, True))


class PageType(models.Model):
    name = models.CharField(u'Name', max_length=128)
    parent = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u"Pagetype")


class TypeArea(LangModel):

    area = models.CharField(max_length=64, choices=settings.AREAS)
    type = models.ForeignKey(PageType)
    widgets = models.ManyToManyField(WidgetAdapter, through="WidgetInArea")

    objects = LangManager()

    def full_clean(self, *args, **kwargs):
        f = TypeArea.objects.filter(
            area=self.area, type=self.type, lang=''
        ).exclude(pk=self.pk)
        if f:
            raise ValidationError({'__all__': ('Language Error',)})
        return super(TypeArea, self).full_clean(*args, **kwargs)

    def __unicode__(self):
        return "%s_%s%s" % (self.area, self.type,
                            ("_%s" % self.lang if self.lang else ""))

    class Meta:
        unique_together = ('area', 'type', 'lang')
        verbose_name = _("Pagetype-Area")
        verbose_name_plural = _("Pagetype-Areas")


class WidgetInArea(models.Model):
    typearea = models.ForeignKey(TypeArea)
    widget = models.ForeignKey(WidgetAdapter, related_name="widget_in_area")
    position = models.PositiveIntegerField()
    enabled = models.BooleanField(u'enabled', default=False)

    def __unicode__(self):
        return u"%s@%s" % (self.widget, self.typearea.type)

    class Meta:
        ordering = ['position']
