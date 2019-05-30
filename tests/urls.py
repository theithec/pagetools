from django.conf.urls import url, include
from django.contrib import admin

from filebrowser.sites import site

from pagetools.pages.views import IndexView

from pagetools.sections.views import admin_pagenodesview

from demo.urls import urlpatterns

urlpatterns += [
    url(r'^$', IndexView.as_view(), name="index"),
]
