'''
Created on 29.05.2013

@author: lotek
'''
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView

from pagetools.gallery.models import Gallery
from pagetools.core.views import BasePagelikeView


class GalleryView(BasePagelikeView, DetailView):
    template_name = "gallery.html"
    model = Gallery
