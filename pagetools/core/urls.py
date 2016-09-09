from django.conf import settings
from django.conf.urls import url
from django.views import static
#  from django.conf.urls.shortcut import urlpatterns

urlpatterns = []
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', static.serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
