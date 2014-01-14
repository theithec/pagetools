from django.conf.urls import url

from .views import GalleryView


urlpatterns = [
    url(r'(?P<slug>[-\w]+)/', GalleryView.as_view(), name="gallerydetailview"),
]
