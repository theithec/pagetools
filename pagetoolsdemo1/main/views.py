from pagetools.sections.views import BaseAjaxNodeView, BaseNodeView
from pagetools.menus.models import MenuEntry
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


def page_entries():
    return [
        MenuEntry(title="Auto1", content_object=SectionPage.objects.first()),
        MenuEntry(title="Auto2", content_object=SectionPage.objects.first()),
    ]
