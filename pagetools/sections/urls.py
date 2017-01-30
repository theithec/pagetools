from django.conf.urls import include, url

from pagetools.sections.views import PagelikeNodeView, BaseAjaxNodeView

app_name = "sections"

urlpatterns = [
   url(r'^ajaxnode/(?P<slug>[-\w]+)/$',
       BaseAjaxNodeView.as_view(), name="ajax"),
   url(r'^(?P<slug>[-\w]+)/$', PagelikeNodeView.as_view(), name="node"),
]
