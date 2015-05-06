from django.shortcuts import render
from pagetools.sections.views import BaseAjaxNodeView, BaseNodeView
from .models import PageNode

class NodeView(BaseNodeView):
    model = PageNode


class IndexView(NodeView):
    template_name = "base.html"

    def get_object(self, *args, **kwargs):
        self.object = PageNode.public.lfilter(node_type='page')[0]
        return self.object


class AjaxNodeView(BaseAjaxNodeView):
    model = PageNode
