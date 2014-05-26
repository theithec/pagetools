from django.conf.urls import patterns, include, url


from . import settings
from pagetools.pages.views import PageView


urlpatterns = patterns('',
   url(r'%s(?P<slug>[-\w]+)/$' % settings.PAGE_PREFIX, PageView.as_view()),
)
