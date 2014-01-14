from django.conf.urls import patterns, url

from pagetools.search.views import SearchResultsView
from pagetools.menus.utils import entrieable_views


urlpatterns = patterns('',
                       
    entrieable_views(url(r'^', (SearchResultsView.as_view()), name=u'search')),

)
