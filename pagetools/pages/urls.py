from django.conf.urls import url

from pagetools.pages.views import PageView

app_name = "pages"
urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', PageView.as_view(), name="pageview"),
]
