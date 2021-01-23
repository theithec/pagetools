from django.conf.urls import url

from pagetools.menus.utils import entrieable_reverse_name
from pagetools.search.views import SearchResultsView

urlpatterns = (url(r"^", (SearchResultsView.as_view()), name=entrieable_reverse_name("search")),)
