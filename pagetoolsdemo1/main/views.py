from pagetools.sections.views import BaseAjaxNodeView, BaseNodeView
from .models import SectionPage, PageNode


class NodeView(BaseNodeView):
    model = PageNode


class IndexView(NodeView):

    template_name = "sections/sections_base.html"

    def get_object(self, *args, **kwargs):
        self.object = SectionPage.objects.filter(
            content_type_pk=SectionPage.get_contenttype_pk()).first()
        return self.object


class AjaxNodeView(BaseAjaxNodeView):
    model = PageNode
