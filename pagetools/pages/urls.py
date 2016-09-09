from django.conf.urls import patterns, include, url


from . import settings
from pagetools.pages.views import PageView, IndexView

app_name="pages"
urlpatterns = [
   # url(r'^$', IndexView.as_view(), name="indexview"),
   url(r'^(?P<slug>[-\w]+)/$', PageView.as_view(), name="pageview"),
]
