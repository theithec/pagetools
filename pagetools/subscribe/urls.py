from django.conf.urls import patterns, url


urlpatterns = patterns('pagetools.subscribe.views',

    url(r'^subscribe', 'subscribe', name="subscribe"),
    url('activate/(?P<key>\w+)/$', 'activate', name='activate'),
    url('unsubscribe/(?P<key>\w+)/$', 'unsubscribe', name='unsubscribe')
)
