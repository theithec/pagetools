from django.conf.urls import url
from pagetools.sections.views impolt BaseNodeView, BaseAjaxNodeView

app_name = 'main'
urlpatterns = [
    #url(r'^sections/(?P<slug>[-\w]+)/$', BaseNodeView.as_view(template_name="sections/page.html")),
    #url(r'^articles/(?P<slug>[-\w]+)/$', BaseNodeView.as_view(template_name="sections/article_detail.html"), name="article"),
]
