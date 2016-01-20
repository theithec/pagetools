Pagetools
=========

Pagetools is a set of Django apps to to provide some cms-like features.

-   menus
-   widgets
-   pages
-   search
-   subscribe/newsletter
-   gallery
-   sections

without changing the way you work with django, provided you use grappelli.

Requirements
------------

    'crispy_forms',
    'grappelli',
    'filebrowser',
    'mptt'


Quick start
-----------

1. Add the apps to your INSTALLED_APPS setting like this::

        INSTALLED_APPS = (

        ...
         'crispy_forms',
        'grappelli',
         #'grappelli-dashboard',
        'filebrowser',
        'mptt',
        'pagetools.core',
        'pagetools.pages',
        'pagetools.widgets',
        'pagetools.menus',
        'pagetools.search',
        'pagetools.subscribe',
        'pagetools.gallery',
        'pagetools.search',
        )

 all submodules need 'pagetools.core',
 'pages' needs 'widgets 'and 'menus', everything else is optional.


2. Include the urls in your project urls.py like this::

        url(r'^', include('pagetools.urls')),
        url(r'^', include('pagetools.pages.urls')),
        url(r'^subscribe/', include('pagetools.subscribe.urls')),
        url(r'^search/', include('pagetools.search.urls')),
        url(r'^gallery/', include('pagetools.gallery.urls')),

3. Run `python manage.py migrate` (or syncdb) to create the  models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Add a Menu, e.g. 'mainmenu'
 After 'save and continue editing', the admin page has a section 'add new entry' containing  'Page', 'Link' and  'PageView' to create objects of those.
 Of cource you can create a (e.g.) page using /admin/pages/add but doing it from the menu  preselects the menu
 for the page and redirect to the menu after saving the page.
 Create a page, make sure it is published (not draft) and 'mainmenu' is selected  in the menus field. Save.
 The page is available under http://127.0.0.1:8000/page/<page_slug>
 Make sure you have something like this in your template:

        {% load menus_tags %}
        ...
        <ul class="mymenu">
        {% menu mainmenu selected %}
        </ul>

 Back in the menu-admin, there is a new menuentry. Select 'show' to make it visible in the menu.

 Items in the menu-admin are drag-and-droppable for ordering (can be nested).
 The menu must be saved to make these changes work.

 Menus can be included to grappellis dashboard with the
 pagetools.menus.dashboard_modules.MenuModule(title="MainMenu")

6. Widgets, Areas, Pagetypes
    Areas are defined in the settings. The default settings are
            (('sidebar', _('Sidebar'),),)
    in `pagetools.widgets.settings.AREAS`.
    Use `PT_AREAS` to define your own.
    Create a pagetype. Use Pagetype-Area->add to create both at once.
    If you name the pagetype "base", it  will be used as a default/fallback.
    If you use "save and continue editing" you can now add widgets.
    Assoc:iate a request with a pagetype:
    - If the view inherits from pagetools.WidgetPagelikeView the views `get_pagetype`
      will be used. It looks for a 'pagetype_name' in context-kwargs, then in the view's attributes.
    - For Pages, which have their own foreign key to `pagetools.widgets.Pagetype`, the `pagetools.pages.views.PageView` overwrites this with

            return self.object.pagetype or WidgetPagelikeView.get_pagetype(self)       
             
    - Or you can just call `pagetools.widgets.utils.get_areas_for_type(pagetype)` yourself and add the result to your context as 'areas'.
    'areas' is a dict with the names of the areas as keys pointing to a list of dicts
    which contains the widget data {'title':"...", 'content' "...", 'type' "..." }.
    - Use something like this your template:

        {% with areas.sidebar as sidebar %}
        {% for w in sidebar %}
            <div class="sidebar-module" %}">
            <h4> {{ w.title|safe }}</h4>
            {{ w.content|safe }}
            </div>
            {% endfor %}
        {%endwith %}

7. Search


    



































