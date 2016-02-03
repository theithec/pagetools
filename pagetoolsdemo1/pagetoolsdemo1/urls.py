from django.conf.urls import include, url
from django.contrib import admin
from filebrowser.sites import site
from main.views import IndexView


urlpatterns = [
    # Examples:
    # url(r'^$', 'pagetoolsdemo1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('pagetools.core.urls')),
    url(r'^', include('pagetools.subscribe.urls')),
    #url(r'^gal/', include('pagetools.gallery.urls')),
    url(r'^search/', include('pagetools.search.urls')),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^', include('pagetools.pages.urls')),
]
