"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'src.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard

from pagetools.menus.dashboard_modules import MenuModule

mainmodels = [

    (_('Structure'),
        ['pagetools.widgets.models.%s' % m for m in (
            'ContentWidget',
            'TemplateTagWidget',
            'TypeArea',
            'PageType',
        )],
        'grp-collapse grp-closed'
     ),

    (_('Content'),
        ['main.models.%s' % m for m in ('News', )] +
        ['pagetools.pages.models.Page', ],
        'grp-collapse grp-closed',  # '' # <-(css-classses)
     ),
]


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):

        self.children.append(MenuModule(column=1,))

        for m in mainmodels:
            self.children.append(
                modules.ModelList(
                    _(m[0]),
                    column=1,
                    models=(m[1]),
                    css_classes=(m[2],),
                ),
            )
        excludedapps = ['django.contrib.*', ]
        for a in [a for a in [m[1] for m in mainmodels]]:
            excludedapps.extend(a)
        self.children.append(
            modules.AppList(
                _('More ...'),
                column=1,
                css_classes=('grp-collapse grp-closed',),
                exclude=excludedapps
            )
        )

        self.children.append(
            modules.AppList(
                _('Administration'),
                column=1,
                css_classes=('grp-collapse grp-closed',),
                models=('django.contrib.*',),
            ),
        )

        self.children.append(modules.LinkList(
            _('Links'),
            column=2,
            children=[
                {
                    'title': _('Zur Webseite'),
                    'url': '/',
                    'external': True,
                    'target': '_blank'
                },
            ]
        ))
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                    'attrs': {'target': '_blank'},
                },
            ]
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'http://packages.python.org/django-grappelli/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Google-Code'),
                    'url': 'http://code.google.com/p/django-grappelli/',
                    'external': True,
                },
            ]
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))
