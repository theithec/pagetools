from django import template
from django.template.loader import render_to_string, get_template, select_template
from django.template import Context, Template
import pdb
from pagetools.sections.utils import get_template_names_for_obj
register = template.Library()
from pagetools.sections import render_node_extradata

#@register.inclusion_tag('cnodes/cnode.html')
class ContentNode(template.Node):
    def __init__(self, obj, user):
        self.object_var = template.Variable(obj)
        self.user_var = template.Variable(user)

    def render(self, context):
        #pdb.set_trace()
        obj =  self.object_var.resolve(context)
        user =  self.user_var.resolve(context)
        real_template = get_template_names_for_obj(obj)
        print ("CONTECT", context)
        print ("extra", render_node_extradata)
        #context.update(render_node_extradata)
        #context['basetemplate'] = 'cnodes/base_node.html'
        for k, v in render_node_extradata.items():
            context[k] = v
        context['object'] = obj
        if obj.positioned_content:
            context['contents'] = obj.ordered_content(user=user)
        if not  obj.enabled:
            context['unpublished'] = True

        return select_template(real_template).render( context)


@register.tag
def render_node(parser, token, *args, **kwargs):
    obj, user = token.contents.split()[1:]
    return ContentNode(obj, user);


@register.filter(name='ordered_content')
def _ordered_content(value, args):
    obj = value
    return obj.ordered_content(user=args)

