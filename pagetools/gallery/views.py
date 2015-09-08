'''
Created on 29.05.2013

@author: lotek
'''
from django.views.generic.detail import DetailView

from pagetools.gallery.models import Gallery
from pagetools.core.views import BasePagelikeView


class GalleryView(BasePagelikeView, DetailView):
    template_name = "gallery/gallery.html"
    model = Gallery
