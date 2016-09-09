from django.conf.urls import url, include
from django.contrib import admin

from filebrowser.sites import site

from pagetools.pages.views import IndexView

from pagetools.sections.views import admin_pagenodesview

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"), # Optional
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url(r'polls/', include('polls.urls', namespace="polls")),
    # url(r'', include('demo_sections.urls', namespace="demo_sections")),
    url(r'', include('pagetools.core.urls')),
    url(r'pages/', include('pagetools.pages.urls', namespace="pages")),
    url(r'^node/', include('pagetools.sections.urls', namespace ="sections")),
    url(r'^adminnodes/(?P<slug>[\w-]+)/$',
         admin_pagenodesview,
         name='admin_pagenodesview'),
    url(r'search/', include('pagetools.search.urls')),
    url(r'subscribe/', include('pagetools.subscriptions.urls', namespace="subscriptions")),
]
