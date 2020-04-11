from django.shortcuts import render

from pagetools.core.views import PaginatorMixin
from demo_sections.models import Article


class ArticleListView(PaginatorMixin):
    paginate_by = 5
    model = Article
