'''
Created on 29.05.2013

@author: lotek
'''
from django.core.urlresolvers import reverse
from django.db import models
from filebrowser.fields import FileBrowseField
from pagetools.models import PagelikeModel
from django.utils.translation import ugettext_lazy as _


class GalleryPic(models.Model):
    title = models.CharField(_('Title'), max_length=512)
    pic = FileBrowseField(
        _(u"Image"),
        max_length=200,
        directory="gallery",
        extensions=[".jpg", ".jpeg", ".gif", ".png"],
        blank=True,
        null=True
    )

    def __unicode__(self):
        return '%s(%s)' % (self.title, self.pic.name)

    def get_absolute_url(self):
        return reverse("artistdetailview", kwargs={'slug': self.slug})

    class Meta():
        verbose_name = _(u'Titled Picture')
        #verbose_name_plural = _(u'Gallery Pic')


class Gallery(PagelikeModel):
    pics = models.ManyToManyField(GalleryPic, through="PicPos")

    def get_pics(self):
        return self.pics.order_by('picpospic')

    def get_safe(self):
        return self

    def get_title(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("gallerydetailview", kwargs={'slug': self.slug})

    class Meta():
        verbose_name = _(u'Galleries')
        verbose_name_plural = _(u'Galleries')


class PicPos(models.Model):
    pic = models.ForeignKey(GalleryPic, related_name="picpospic")
    gal = models.ForeignKey(Gallery)
    position = models.PositiveIntegerField() 
    
    class Meta():
        verbose_name = _(u'Positioned Picture')
