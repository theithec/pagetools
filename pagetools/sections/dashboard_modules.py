from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlquote
from django.utils.html import format_html
from grappelli.dashboard.modules import DashboardModule
from .models import PageNode
#from grappelli.dashboard.utils import get_admin_site_name
#from pagetools.menus.models import Menu
#from pagetools.menus.utils import entrieable_models
#from pagetools.core.utils import get_classname
#from django.core.exceptions import MultipleObjectsReturned


class PageNodesModule(DashboardModule):
    """
    A module that displays a page with nodes.
    A "page" should be the root-pagenode model.
    Overwrite model =  <YourModel>
    
    Dashboard needs to include the static files, e.g:
    ----------------------------------------------------------------------------
    def _media(self):
            return forms.Media(
                js=["bower_components/jquery/dist/jquery.min.js",
                    "bower_components/jquery-bonsai/jquery.bonsai.js",
                    "js/nodetree.js"
                    ],
                css = {'all': ['bower_components/jquery-bonsai/jquery.bonsai.css ']}
            )

    media = property(_media)
    ----------------------------------------------------------------------------

    """

    model = PageNode
    template = 'admin/dashboard_pagenodes_module.html'

    def __init__(self, *args, **kwargs):
        kwargs['title'] = "Nodes Tree"
        super(PageNodesModule, self).__init__(*args, **kwargs)

    def init_with_context(self, context):
        pages = self.model.objects.all()
        context['pages'] = pages
        context['admin_pagenodesview'] = reverse(
            'admin_pagenodesview',
            args = ('__SLUG__', )) 
        options=""
        for p in pages:
            options += format_html(
                '<option name={}>{}</option>' ,p.pk, p.title)
        self.pre_content = '''<label>
            Page
            </label>
            <select style="width: auto;" id='pagenode_page_chooser'>
                %s
            </select>''' % options
        
        super(PageNodesModule, self).init_with_context(context)
        self._initialized = True
