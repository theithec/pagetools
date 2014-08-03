# Create your views here.
from django.views.generic.dates import MonthArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from pagetools.core.views import BasePagelikeView

from .models import News


class NewsView(BasePagelikeView):
    queryset = News.public.lfilter()


class NewsListView(NewsView, ListView):
    pass


class NewsDetailView(NewsView, DetailView):
    pass


class NewsMonthArchiveView(NewsView, MonthArchiveView):
    date_field = "status_changed"
    make_object_list = True
    allow_future = True
