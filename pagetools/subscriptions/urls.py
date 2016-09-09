from django.conf.urls import url
from .views import activate, subscribe, unsubscribe

app_name = "subscriptions"

urlpatterns = [
    url(r'^subscribe/', subscribe, name="subscribe"),
    url('^activate/(?P<key>\w+)/$', activate, name='activate'),
    url('^unsubscribe/(?P<key>\w+)/$', unsubscribe, name='unsubscribe')
]
