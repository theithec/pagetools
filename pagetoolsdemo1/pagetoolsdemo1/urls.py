from django.conf.urls import include, url
from django.contrib import admin
from filebrowser.sites import site
from pagetools.menus.utils import entrieable_reverse_name
from main.views import IndexView, page_entries


urlpatterns = [
    # Examples:
    # url(r'^$', 'pagetoolsdemo1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('pagetools.core.urls')),
    url(r'^', include('pagetools.subscribtions.urls')),
    #url(r'^gal/', include('pagetools.gallery.urls')),
    url(r'^search/', include('pagetools.search.urls')),
    url(r'^$', IndexView.as_view(), name=entrieable_reverse_name('index', auto_children=page_entries)),
    url(r'^', include('pagetools.pages.urls')),
]
