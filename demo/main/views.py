from pagetools.views import PaginatorMixin
from demo_sections.models import Article


class ArticleListView(PaginatorMixin):
    paginate_by = 5
    model = Article
