from django.conf.urls import patterns, include, url


from . import settings
from pagetools.pages.views import PageView, IndexView


urlpatterns = [
   url(r'^$', IndexView.as_view(), name="indexview"),
   url(r'^%s(?P<slug>[-\w]+)/$' % settings.PAGE_PREFIX, PageView.as_view(), name="pageview"),
]
