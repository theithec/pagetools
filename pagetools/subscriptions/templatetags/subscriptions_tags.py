'''
Created on 29.02.2012

@author: Tim Heithecker
'''

from django import template

from pagetools.subscriptions.forms import SubscribeForm


register = template.Library()


class NewsSubscribtionNode(template.Node):

    def render(self, context):
        t = template.loader.get_template('subscriptions/block_subscribtion.html')
        context['sform'] = SubscribeForm()
        return t.render(context)


@register.tag(name="subscribe_widget")
def do_news_subscribtion(parser, token):
    return NewsSubscribtionNode()



