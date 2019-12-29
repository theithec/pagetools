'''
Created on 29.02.2012

@author: Tim Heithecker
'''

from django import template

from pagetools.subscriptions.forms import SubscribeForm


register = template.Library()


class SubscribeNode(template.Node):

    def render(self, context):
        t = template.loader.get_template(
            'subscriptions/block_subscription.html')
        context['sform'] = SubscribeForm()
        return t.render(context.flatten())


@register.tag(name="subscribe_widget")
def do_subscribe_node(parser, token):
    return SubscribeNode()
