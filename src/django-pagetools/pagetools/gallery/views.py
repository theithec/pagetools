'''
Created on 29.05.2013

@author: lotek
'''
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView

from pagetools.gallery.models import Gallery


class GalleryView(DetailView):
    template_name = "gallery.html"
    model = Gallery

    # def get_object(self, **kwargs):
    #    return get_object_or_404(
    #        Gallery.objects.filter(slug=self.kwargs['slug']))
