.. _widgets:

=======
Widgets
=======

Introducion
-----------

This app is about showing different additional content for different pages.
The additional content(the widgets) is shown in "areas" which, are defined in settings::

    AREAS = getattr(settings, 'PT_AREAS',
                (('sidebar', _('Sidebar'),),)
                )

and in the template(s)::


    {% for widget in areas.sidebar %}
    {{ widget|safe }}
    {% endfor %}

Next, there is `Pagetype`, which is a small model with a name and and an optional another pagetype as parent.
Pagetypes and areas gets combined trough the `TypeArea` model, which is where the widgets are organized,
so the content of an area can be different for different pagetypes.

In code::
    
    from pagetools.widgets.models import *
    from pagetools.widgets.utils import get_areas_for_type

    pt1 = PageType.objects.create(name="pt1")
    ta1 = TypeArea.objects.create(pagetype=pt1, area="sidebar")

    w1 = ContentWidget.objects.create(name="w1", content="Foo")
    wia1 = WidgetInArea.objects.create(content_object=w1, typearea=ta1, position=1, enabled=True)

    get_areas_for_type(pt1, {})
    >> {'sidebar': ['\nFoo\n']}

Admin
-----

In the backend, most things can be done in the PageType admin.
All subclasses of `BaseWidget` are listed in the "Add Widget" section.
Other Classes may be added also, as long as they have a `render` callable and a unique `name` attribute, through the `WidgetInArea` (Included Widgets) admin.

WidgetPagelikeMixin
-------------------

To define a pagetype 

- add a 'pagetype_name' to the context_data or
- define `pagetype_name` or
- overwrite `get_pagetype_name()`


ContextProcessors
-----------------

In `pagetools.widgets.context_processors`

- base_pagetype
  Uses the pagetype named "base"

- pagetype_from_view
  Tries to find an attribute "pagetype_name" in the view.
  (So this is possible: thirdparty.views.FooView.pagetype_name="special")

Some notes:
-----------

- Pagetypes can be nested, however this is only useful if you have multiple areas (e.g. sidebar and header).
- A Pagetype called "base" will be used as default/fallback if exists.

- Creating custom widget classes is easy. A templatetag class that doesn't require arguments can just be added
  to the `PT_TEMPLATETAG_WIDGETS` setting.


