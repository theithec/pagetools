from django import template

from pagetools.subscriptions.forms import SubscribeForm


register = template.Library()


class SubscribeNode(template.Node):

    def render(self, context):
        t = template.loader.get_template(
            'subscriptions/block_subscription.html')
        context['sform'] = SubscribeForm()
        try:
            context = context.flatten()
        except AttributeError:
            pass

        return t.render(context)


@register.tag(name="subscribe_widget")
def do_subscribe_node(parser, token):
    return SubscribeNode()
