from django.conf.urls import patterns, include, url
from django.contrib import admin

from filebrowser.sites import site as filebrowser_site
from pagetools.core.urls import urlpatterns as pt_urlpatterns
from pagetools.pages.views import IndexView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/filebrowser/', include(filebrowser_site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view()),
    url(r'^', include('pagetools.core.urls')),
    url(r'^', include('pagetools.pages.urls')),
    url(r'^subscribe/', include('pagetools.subscribe.urls')),
    url(r'^search/', include('pagetools.search.urls')),
    url(r'^gallery/', include('pagetools.gallery.urls')),
) + pt_urlpatterns