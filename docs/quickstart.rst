.. _quickstart:

==========
Quickstart
==========

Setup
~~~~~

It's more interesting to show how pagetools works with existing apps.
But let's start with a pure pagetools installation.


Add the pagetools apps you want to use and their requirements to ``INSTALLED_APPS``::

        INSTALLED_APPS = [
            'grappelli.dashboard',# optional (pagetools provides two dashboard modules), needs further configuration
            'grappelli',
            'django.contrib.admin',
            ...
            'django.contrib.sites',
            'crispy_forms',      # required for pages
            'sekizai',           # required for sections. Needs further configuration
            'pagetools.core',    # needed for all pagetools modules
            'pagetools.widgets', # Widgets (e.g. for sidebars)
            'pagetools.menus',   #
            'pagetools.pages',   # Simple Pages, requires menus and widgets
            'pagetools.sections',# Nested Content (e.g. for a singlepage site)
            'pagetools.search',  # Simple Search on database fields
            'pagetools.subscriptions', # Subscriptions to whatever
            ...
          ]

          SITE_ID = 1  # required by contrib.sites


Add the urls to your project::

        #  for the section dashboard module
        #  from pagetools.sections.views import admin_pagenodesview

        # Optional
        from pagetools.pages.views import IndexView

        url_patterns = [
            url(r'^$', IndexView.as_view()), # Optional
            url(r'^grappelli/', include('grappelli.urls')),
            url(r'^admin/', admin.site.urls),
            ...
            url(r'pages/', include('pagetools.pages.urls')),
            url(r'^node/', include('pagetools.sections.urls')),
            # url(r'^adminnodes/(?P<slug>[\w-]+)/$',
            #     admin_pagenodesview,
            #     name='admin_pagenodesview'),
            url(r'search/', include('pagetools.search.urls')),
            url(r'subscribe/', include('pagetools.subscriptions.urls')),
            ...
        ]



.. _dashboard :

Configuring the Dashboard
^^^^^^^^^^^^^^^^^^^^^^^^^

Migrate if you have not already..

Create the dashboard::

        ./manage.py customdashboard

and add it in settings::


        GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'


Edit `dashboard.py` to include the menu module::

        from pagetools.menus.dashboard_modules import MenuModule
        ...

        class CustomIndexDashboard(Dashboard):
                ...
                def init_with_context(self, context):
                        ...
                        self.children.append(MenuModule(column=1)) # default menu title is MainMenu
                        # or
                        # self.children.append(MenuModule(column=1, menu_title="mymenu"))




Create a menu with a page
~~~~~~~~~~~~~~~~~~~~~~~~~

Click on ``Menu not found. Create`` in the Menu Module.
After ``Save and continue editing`` you can add entries to the menu.

Add a :doc:`Page <pages>` to the menu. Set status to published, give it a title and some content.
Make sure under `Menus` your menu is selected. Save and return to the menu.


Select ``Show`` for your new menu entry and save the menu.


Call the menu in your template::

        {% load [...] menus_tags %}
        ...

        <ul>
                {% menu MainMenu menukeys%}
        </ul>


`MainMenu` is the internal name of the menu, `menuykeys` is a contextvariable set to the slugs of the menuentries related to the current page (if any).

Some notes:

- Views can be added to the menu trough the `ViewLink` class. See :doc:`Search <search>` for an example.
- You are not restricted to the models listed on the menu admin. Everything with an `get_absolute_url` callable  may be allowed as an entry. See :ref:`menuentrieables`. Entries may be created dynamically.
- Note that entries may be nested (just drag and drop).
- Use a `Link` to "#" if you want a dummy parent entry.
- The menu template may be overwritten in settings.
- The pagetools templates expects a `base.html` template with `{% block main %}`, `{% block css %}` and `{% block js %}`.
- If the slug of the page is "start", the `pages.IndexView` will use it.
- Most pagetools models have a language field. If you don't need different languages just ignore them.



Widgets - Create a sidebar
~~~~~~~~~~~~~~~~~~~~~~~~~~

The idea:

1. Some parts of the base template are defined as `areas`. An area may be a sidebar with some boxes or just a background picture.
   Areas are defined in settings. It make no sense to add areas on the fly because they have to be defined in the template also.
2. Somewhere in your views or your model or your object you define `pagetypes`.
   Pagetypes may be created dynamically or in code.
3. Combine areas and pagetypes to define what additional content is shown for your view (or object - or model, depends on your implementation).

Add something like this to your base template.::

        <sidebar>
                {% with areas.sidebar as widgets %}
                {% for widget in widgets %}
                {% if widget.title %}<h4>{{widget.title}}</h4>{% endif %}
                {{ widget.content|safe }}
                {% endfor %}
                {% endwith %}
        </sidebar>

Go to admin->widgets->Pagetype-Areas. Select the one default area named "sidebar". Create a Pagetype and call it "base".
`Save and continue editing`. Add a Content Widget. The name is the internal name for the widget. Save and return to the Pagetype-Area. Enable the new widget. Save.

A `PageType` called  `base` is used as the default/fallback pagetype, therefor the widget is visible.

You could create a new `Pagetype-Area` with a new `Pagetype`, e.g. named 'special' with different widgets and change the pagetype of the former created page to the new type.


Some notes:

- Pagetypes can be nested, however this is only useful if you have multiple areas (e.g. sidebar and header).
- Creating custom widget classes is easy. If you have a templatetag that doesn't require arguments, you can just add it
  to the `PT_TEMPLATETAG_WIDGETS` setting.
- To enable the whole thing, somewhere `pagetools.widgets.utils.get_areas_for_type("pagetypename", kwargs)` must be integrated
  in the template context(e.g. as `areas`) where `kwargs` will be passed to the included  widgets `get_content` call.


Search
~~~~~~

The search is just a simple database query.
Define somwhere::

        from pagetools import search

        search.search_mods = (
               (Page, ('title', 'content'),),
               # or
               # (Page, ('title', 'content'),{'replacements': 'content'}),
                ...
        )


If replacement is defined as a json file, it will be used as source for replacements.
(e.g. "&auml;" to "ä").
You can also set search.extra_filter to a callable that receives the resulting queryset (and should return one)

The SearchView is also an example for adding a view to the Menu.
All is required is a call to pagetools.menus.utils.entrieable_reverse_name with one or two arguments (viewname, appname).
Because the function returns the viewname, this can be done in the urls::

        urlpatterns = [

        url(r'^', (SearchResultsView.as_view()), name=entrieable_reverse_name('search', app_name="search")),
        # or - if no app_name is used
        # url(r'^', (SearchResultsView.as_view()), name=entrieable_reverse_name('search')),



Sections
~~~~~~~~

This is for nested content, e.g. to build a typical singe-page structure with sections like portfolio, team, and contact.


Go to "Your Menu" -> Add -> Section-Page. Give the page a title and ``Save and continue editing``.
In the  ``Positioned Content``-area click on the "+" to add a section. Give the section also a title and save and continue.
In the section you can add articles.

