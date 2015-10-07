'''
Created on 29.05.2013

@author: lotek
'''
from django.core.urlresolvers import reverse
from django.db import models
from filebrowser.fields import FileBrowseField
from pagetools.core.models import PagelikeModel
from django.utils.translation import ugettext_lazy as _


class GalleryPic(PagelikeModel):
    pic = FileBrowseField(
        _("Image"),
        max_length=200,
        directory="gallery",
        extensions=[".jpg", ".jpeg", ".gif", ".png"],
        blank=True,
        null=True
    )

    def __str__(self):
        return '%s(%s)' % (self.title, self.pic.name)

    class Meta():
        verbose_name = _('Titled Picture')
        verbose_name = _('Titled Pictures')


class BaseGallery(models.Model):

    def get_pics(self):
        return self.pics.order_by('positioned_pic')

    def get_title(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("gallerydetailview", kwargs={'slug': self.slug})

    class Meta():
        verbose_name = _('Galleries')
        verbose_name_plural = _('Galleries')
        abstract = True

class Gallery(BaseGallery, PagelikeModel):
    pics = models.ManyToManyField(GalleryPic, through="PicPos")

class BasePicPos(models.Model):
    position = models.PositiveIntegerField()

    class Meta():
        verbose_name = _('Picture')
        verbose_name_plural = _('Pictures')
        abstract = True


class PicPos(BasePicPos):
    gal = models.ForeignKey(Gallery)
    pic = models.ForeignKey(GalleryPic, related_name="positioned_pic")

    class Meta():
        verbose_name = _('Positioned Picture')


