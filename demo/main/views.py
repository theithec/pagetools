from pagetools.views import PaginatorMixin
from demo_sections.models import Article


class ArticleListView(PaginatorMixin):
    paginate_by = 5
    model = Article
    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     data["form"] = FooForm()
    #     return data
