from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard.modules import DashboardModule
from grappelli.dashboard.utils import get_admin_site_name
from pagetools.menus.models import Menu
from pagetools.menus.utils import entrieable_models
from pagetools.utils import get_classname
from django.core.exceptions import MultipleObjectsReturned

class MenuModule(DashboardModule):
    """
    A module that displays a pagettools.menus.menu.
    
     in dashboard: 
     self.children.append(MenuModule(menu_title='myMenu', column=1,))
    
    """

    template = 'admin/dashboard_menu_module.html'

    def __init__(self, *args, **kwargs):
        self.menu_title = kwargs.pop('menu_title', 'MainMenu')
        kwargs['title'] = kwargs.get('title',
            u'%s: %s' % (_('Menu Overview'), self.menu_title))
        super(MenuModule, self).__init__(*args, **kwargs)
        
        
    def add_entrychildren(self, children, collected=None):
        if collected == None:
            collected = []
        for c in children:
            print c
            c['url'] = c['obj_admin_url'] + '?menu=%s'% self.menu.pk
            collected.append(c)
            cc = c.get('children', None)
            if cc:
                collected = self.add_entrychildren(cc, collected)
        return collected

    def init_with_context(self, context):
        try:
            self.menu = Menu.objects.lfilter().get(title=self.menu_title)
        except (Menu.DoesNotExist, MultipleObjectsReturned),e:
            self.pre_content = 'Menu not found'
            return
        context['menu'] = {
            'name': self.menu,
            'url': reverse("admin:menus_menu_change",args=[self.menu.pk])

        }
        nested_children = self.menu.children_list(for_admin=True)
        context['existing'] = self.add_entrychildren(nested_children)
        emods = entrieable_models()
        for em in emods:
            self.children.append({
                'name': get_classname(em),
                'url': reverse("admin:%s_%s_add" % (
                    em.__module__[:-7].split('.')[-1],
                    em.__name__.lower()
                )) + '?menu=%s'% self.menu.pk
            })
        super(MenuModule, self).init_with_context(context)
        self._initialized = True