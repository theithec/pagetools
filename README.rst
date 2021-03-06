.. |travisbadge| image:: https://travis-ci.org/theithec/django-pagetools.svg?branch=master
.. _travisbadge: https://travis-ci.org/theithec/django-pagetools

.. |coverallsbadge| image:: https://coveralls.io/repos/github/theithec/django-pagetools/badge.svg?branch=master
.. _coverallsbadge: https://coveralls.io/github/theithec/django-pagetools/


|travisbadge|_ |coverallsbadge|_


Welcome to django-pagetools's documentation!
============================================

**Django-pagetools** is a set of Django apps to provide some cms-like features

-   Menus
-   Widgets
-   Pages (with forms)
-   Subscribtions/Newsletter
-   Sections (nested content)
-   Search

without changing the workflow with Django, provided you use Grappelli.


**Documentation (WIP)**: https://django-pagetools.readthedocs.io/en/latest/


**Demo**::
  
    git clone git+https://theithec/django-pagetools.git

    cd django-pagetools/

    python setup.py install

    cd demo

    ./manage.py migrate

    ./manage.py createdemodata

    ./manage.py runserver

| Admin-url: http://127.0.0.1:8000/admin
| User:      admin  
| Password:  password

