from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.shortcut import urlpatterns


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
