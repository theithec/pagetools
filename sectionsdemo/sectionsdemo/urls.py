from django.conf.urls import patterns, include, url
from django.contrib import admin
from filebrowser.sites import site
from main.views import IndexView


urlpatterns = patterns('',
    # Examples:
    url(r'^$', IndexView.as_view(), name='index'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
