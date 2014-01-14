from django.conf.urls import patterns, url

from pagetools.search.views import SearchResultsView
from pagetools.menus.utils import entrieable_view


urlpatterns = patterns('',
    entrieable_view(url(r'^', (SearchResultsView.as_view()), name='search')),
)
