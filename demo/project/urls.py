from django.conf.urls import patterns, include, url
from django.contrib import admin

from filebrowser.sites import site as filebrowser_site

from pagetools.core.urls import urlpatterns as pt_urlpatterns

from main.views import NewsListView, NewsDetailView, NewsMonthArchiveView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/filebrowser/', include(filebrowser_site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', NewsListView.as_view()),
    url(r'news/(?P<slug>[-\w]+)/$', NewsDetailView.as_view(), name='news_detail'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',
        NewsMonthArchiveView.as_view(),
        name="archive_month"),
    url(r'^', include('pagetools.pages.urls')),
    url(r'^subscribe/', include('pagetools.subscribe.urls')),
    url(r'^search/', include('pagetools.search.urls')),
    url(r'^gallery/', include('pagetools.gallery.urls')),
) + pt_urlpatterns
