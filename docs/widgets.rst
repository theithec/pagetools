.. widgets_

Widgets
~~~~~~~

This is about showing different additional content for a page.
Connenect widgets to areas through pagetypes
A `Widget` contains some kind of content.
A `Pagetype` is a small model with a name and and an optional other pagetype as parent. A `Pagetype` named `base` will be used as default/fallback.
`Areas` are defined in settings::

    AREAS = getattr(settings, 'PT_AREAS',
                (('sidebar', _('Sidebar'),),)
                )

A `PagetypeArea` contains both, a pagetype and an area and widgets can be added to it through a `WidgetInArea`.

`pagetools.views.WidgetPagelikeMixin` tries
- 'pagetype_name' in context_data
- self.pagetype_name
- self.get_pagetype_name()
- self.get_pagetype(pagetypename=None)

to find a pagetype as an argument for :func:`pagetools.widgets.utils.get_areas_for_type`. The result gets added to the context_data as a dict named 'areas'.::

    {
        'sidebar':[
            {'content':'Foo'},
            {'content':'Bar'}
            ],
        # other areas ....
    }

The content fields are the result of the widgets `get_content` call.
Note: The context_data that already exits gets passed to `get_content`.

Everything that has an





The WidgetViewMixin.get_context_data tries to find an argument for this function calling self.get_pagetype with the result of self.get_pagetype_name.




from context_data or it's own attributes, then calls get_pagetype with that.




looking forit self having an atrribute 'pagetype_name'

looks for a `pagetype_name` and tries to get a pagetype object form it,
otherwise it looks i




    class WidgetPagelikeMixin(WidgetViewMixin):
A pagetype could be defined per object

    pagetype = models.ForeignKey(PageType, blank=True, null=True)


Examples::

    # pagetools.pages.models.Page

    # pagetype defined in the object
    pagetype = models.ForeignKey(PageType, blank=True, null=True)


    # pagetools.pages.views.PageView

    # .. or in a view
    def get_pagetype(self, **kwargs):
        return self.object.pagetype or super().get_pagetype(self)


    # pagetools.widgets.views.WidgetPagelikeMixin:

        def get_context_data(self, **kwargs):
        ... # for forms in widgets
        if kwargs.get("request", None) is None:
            kwargs.update(csrf(self.request))
        kwargs['areas'] = get_areas_for_type(pt, kwargs)
        kwargs['pagetype_name'] = ptname





`Widgets` are pieces of content that can be added to a `PagetypeArea` instance.
The idea:
In the

A widget is a models with a 'content' field.
A Pagetype is
