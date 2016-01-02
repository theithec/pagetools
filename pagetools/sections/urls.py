
from django.conf.urls import patterns, include, url

from pagetools.sections.views import BaseNodeView, BaseAjaxNodeView

app_name="sections"

urlpatterns = [
   url(r'(?P<slug>[-\w]+)/$', BaseNodeView.as_view(), name="node"),
   url(r'ajaxnode/(?P<slug>[-\w]+)/$', BaseAjaxNodeView.as_view(), name="ajax"),
]
