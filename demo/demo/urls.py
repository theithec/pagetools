from django.urls import path
from django.conf import settings

from django.conf.urls import url, include
from django.contrib import admin

from filebrowser.sites import site

from pagetools.pages.views import IndexView
from pagetools.sections.views import admin_pagenodesview

from main.views import ArticleListView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),  # Optional
    url(r'^admin/filebrowser/', site.urls),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url(r'polls/', include('polls.urls', namespace="polls")),
    # url(r'', include('demo_sections.urls', namespace="demo_sections")),
    url(r'', include('pagetools.urls')),
    url(r'pages/', include('pagetools.pages.urls', namespace="pages")),
    url(r'articles/', ArticleListView.as_view(), name="articles"),
    url(r'^node/', include('pagetools.sections.urls', namespace="sections")),
    url(r'^adminnodes/(?P<slug>[\w-]+)/$',
        admin_pagenodesview,
        name='admin_pagenodesview'),
    url(r'search/', include('pagetools.search.urls')),
    url(r'subscribe/', include('pagetools.subscriptions.urls', namespace="subscriptions")),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
