from django.shortcuts import render
from django.shortcuts import render
from pagetools.sections.views import BaseAjaxNodeView, BaseNodeView
from .models import SectionPage, PageNode


class NodeView(BaseNodeView):
    model = PageNode


class IndexView(NodeView):

    template_name = "sections_base.html"

    def get_object(self, *args, **kwargs):
        self.object2 = SectionPage.objects.filter(
            content_type_pk=SectionPage.get_contenttype_pk()).first()
        self.object = SectionPage.objects.first()
        return self.object


class AjaxNodeView(BaseAjaxNodeView):
    model = PageNode
