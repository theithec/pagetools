'''
Created on 29.05.2013

@author: lotek
'''
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView

from pagetools.gallery.models import Gallery
from pagetools.views import BasePageView

class GalleryView(BasePageView, DetailView):
    template_name = "gallery.html"
    model = Gallery
