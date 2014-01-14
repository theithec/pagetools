=========
Pagetools
=========

Pagetools is a set of Django apps to to provide some cms-like features. 
- menus
- widgets
- gallery 
- pages
- search
- subscribe
 

Detailed documentation is NOT in the "docs" directory.

Quick start
-----------

1. Add the apps to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
    	...
        'pagetools',
        'pagetools.widgets',
        'pagetools.menus',
        'pagetools.pages',
		...        
    )
	
	
	'pages' needs 'widgets 'and 'menus',
   
   

	 
2. Include the urls in your project urls.py like this::

	[depends on the app]
	
3. Run `python manage.py migrate` to create the  models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a menu, page, widget, area, gallery (you'll need the Admin app enabled).
   A simple site with a main-menu could be administrated mainly via the main-menus adminpage.
   
   

