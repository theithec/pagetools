from django.conf.urls import patterns, url

from .views import GalleryView


urlpatterns = patterns('',
    url(r'(?P<slug>[-\w]+)/', GalleryView.as_view(), name="gallerydetailview"),
)
