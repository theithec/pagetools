from django.conf.urls import url

from pagetools.sections.views import BaseAjaxNodeView, PagelikeNodeView

app_name = "sections"

urlpatterns = [
    url(r"^ajaxnode/(?P<slug>[-\w]+)/$", BaseAjaxNodeView.as_view(), name="ajax"),
    url(r"^(?P<slug>[-\w]+)/$", PagelikeNodeView.as_view(), name="node"),
]
