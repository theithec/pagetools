=========
Pagetools
=========

Pagetools is a set of Django apps to to provide some cms-like features.

- menus
- widgets
- pages
- search
- subscribe/newsletter
- gallery 

without changing the way you work with django, provided you use grappelli.

Detailed documentation is MISSING in the "docs" directory.

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
        'mptt'
        'pagetools',
        'pagetools.widgets',
        'pagetools.menus',
        'pagetools.pages',
		...        
    )
 
 all submodules need 'pagetools',   
 'pages' needs 'widgets 'and 'menus',

	 
2. Include the urls in your project urls.py like this::

    url(r'^', include('pagetools.urls')),
    url(r'^', include('pagetools.pages.urls')),
    url(r'^subscribe/', include('pagetools.subscribe.urls')),
    url(r'^search/', include('pagetools.search.urls')),
    url(r'^gallery/', include('pagetools.gallery.urls')),
	
3. Run `python manage.py migrate` to create the  models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   
5. Add a Menu, e.g. 'mainmenu'


    

 After 'save and continue editing', the admin page has a section 'add new entry' conatining  'Page', 'Link' and  'PageView' to create objects of those.
 Of cource you can create a (e.g.) page using /admin/pages/add but doing it from the menu  preselects the menu 
 for the page and redirect to the menu after saving the page.
 Create a page, make sure it is published (not draft) and 'mainmenu' is selected  in the last field of the crispy_forms. Save.
 The page is available under http://127.0.0.1:8000/page/<page_slug>
 Make sure you have this in your template:
 
 ::  
 
    {% load menus_tags %}
    ...
    {% menu mainmenu selected %}    
   
 Back in the menu-admin, there is a new menuentry. select 'show' to make it visible in the menu.
   
 If there are more than one items in the menu-admin, they are are drag-and-droppable for ordering (can be nested).
 The menu must be saved to make these changes work.
   
6. Add an Area
   

   
   
   
   
   
   
   
   
   
   
   

   
   
   
   
   

