'''
Created on 14.12.2013

@author: lotek
'''

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect

from pagetools.core.utils import itersubclasses, get_classname
from pagetools.widgets.models import TypeArea, ContentWidget, PageType, \
    WidgetInArea, BaseWidget, TemplateTagWidget
from pagetools.core.admin import TinyMCEMixin


class WidgetInAreaAdmin(admin.TabularInline):
    model = WidgetInArea
    fields = ("widget", "enabled", "position")
    sortable_field_name = "position"
    extra = 1


class TypeAreaAdmin(admin.ModelAdmin):
    inlines = (WidgetInAreaAdmin,)
    save_as = True

    def render_change_form(self, request, context, add=False,
                           change=False, form_url='', obj=None):
        if obj:
            clslist = list(itersubclasses(BaseWidget))[:]
            context['addable_widgets'] = "".join([
                '<li><a href="' + 
                (reverse('admin:%s_%s_add' % (
                    c._meta.app_label, c._meta.module_name)) + "?typearea=%s" % (context['object_id'])
                ) + '">%s</a></li>' % (get_classname(c))
                for c in clslist
            ])
        else:
            self.change_form_template = 'admin/change_form_help_text.html'
            context['help_text'] = '[save] before adding widgets'
        return admin.ModelAdmin.render_change_form(self, request, context,
                                                   add=add, change=change,
                                                   form_url=form_url, obj=obj)


class BaseWidgetAdmin(admin.ModelAdmin):
    def _redirect(self, action, request, obj, *args, **kwargs):
        s = request.GET.get('typearea', None)
        if s and '_save' in request.POST:
            return HttpResponseRedirect(
                reverse("admin:widgets_typearea_change", args=(s,))
            )
        else:
            return getattr(super(BaseWidgetAdmin, self), "response_%s" % action)(
                request, obj, *args, **kwargs
            )

    def response_add(self, request, obj, *args, **kwargs):
        return self._redirect("add", request, obj, *args, **kwargs)

    def response_change(self, request, obj, *args, **kwargs):
        return self._redirect("change", request, obj, *args, **kwargs)


class ContentWidgetAdmin(BaseWidgetAdmin, TinyMCEMixin):
    pass


class TemplateTagWidgetAdmin(BaseWidgetAdmin):
    prepopulated_fields = {"name": ("renderclasskey",)}


admin.site.register(TypeArea, TypeAreaAdmin)
admin.site.register(ContentWidget, ContentWidgetAdmin)
admin.site.register(TemplateTagWidget, TemplateTagWidgetAdmin)
admin.site.register([PageType])
