from django.conf.urls import patterns, url

from pagetools.search.views import SearchResultsView
from pagetools.menus.utils import entrieable_reverse_name


urlpatterns = patterns('',
    url(r'^', (SearchResultsView.as_view()), name=entrieable_reverse_name('search')),
)
