from django.conf.urls import patterns, include, url
from django.contrib import admin
from pagetools.pages.views import IndexView
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demo2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', IndexView.as_view(), name='index'),
    #url(r'^', include('pagetools.core.urls')),
    url(r'^', include('pagetools.pages.urls')),
    url(r'^subscribe/', include('pagetools.subscribe.urls')),
    url(r'^search/', include('pagetools.search.urls')),
    url(r'^gallery/', include('pagetools.gallery.urls')),


    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
