from django.core.urlresolvers import reverse
from grappelli.dashboard.modules import DashboardModule
from grappelli.dashboard.utils import get_admin_site_name
from pagetools.utils import get_classname
from pagetools.menus.models import Menu
from pagetools.menus.utils import entrieable_models
from django.utils.translation import ugettext_lazy as _


class MenuModule(DashboardModule):
    """
    A module that displays a pagettools.menus.menu.
    
     in dashboard: 
     self.children.append(MenuModule(menu_name='myMenu', column=1,))
    
    """

    template = 'admin/dashboard_menu_module.html'

    def __init__(self, *args, **kwargs):
        self.menu_name = kwargs.pop('menu_name', 'MainMenu')
        kwargs['title'] = kwargs.get('title',
            u'%s: %s' % (_('Menu Overview'), self.menu_name))
        super(MenuModule, self).__init__(*args, **kwargs)

    def init_with_context(self, context):
        try:
            menu = Menu.tree.get(title=self.menu_name)
        except Menu.DoesNotExist:
            self.pre_content = 'Menu not found'
            return
        context['menu'] = {
            'name': menu.title,
            'url': reverse("admin:menus_menu_change",args=[menu.pk])

        }
        context['existing'] = menu.children_list(for_admin=True)
        emods = entrieable_models()
        for em in emods:
            self.children.append({
                'name': get_classname(em),
                'url': reverse("admin:%s_%s_add" % (
                    em.__module__[:-7].split('.')[-1],
                    em.__name__.lower()
                )) + '?menu=%s'% menu.pk
            })
        super(MenuModule, self).init_with_context(context)
        self._initialized = True