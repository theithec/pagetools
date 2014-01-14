'''
Created on 09.05.2013

@author: lotek
'''
from django import  template
from django.core.exceptions import ObjectDoesNotExist
from pagetools.menus.models import Menu

register = template.Library()


class MenuRenderer(template.Node):
    def __init__(self, selected, menu_title):
        self.selected = template.Variable("selected")
        self.menu_title = menu_title

    def render(self, context):
        selected = []
        try:
            selected = self.selected.resolve(context)

        except template.VariableDoesNotExist:
            pass
        try:
            menu = Menu.objects.lfilter().get(title=self.menu_title)
        except  ObjectDoesNotExist:
            e = "<!--UNKNOWN MENU %s !-->" % self.menu_title
            return e
        return menu.render(selected)


@register.tag(name="menu")
def do_menu(parser, token):
    menu_title, selected = token.contents.split()[1:]
    return MenuRenderer(selected, menu_title)


