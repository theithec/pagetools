'''
Created on 14.12.2013

@author: lotek
'''

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect

from pagetools.core.admin import TinyMCEMixin
from pagetools.core.utils import itersubclasses, get_classname
from .models import TypeArea, ContentWidget, PageType, \
    WidgetInArea, BaseWidget, TemplateTagWidget


class WidgetInAreaAdmin(admin.TabularInline):
    model = WidgetInArea
    fields = ("adminedit_url", "enabled", "position",)
    sortable_field_name = "position"
    extra = 1
    max_num = 1
    readonly_fields = ( "adminedit_url",)


class TypeAreaAdmin(admin.ModelAdmin):
    inlines = (WidgetInAreaAdmin,)
    save_as = True

    def save_model(self, request, obj, form, change):
        super(TypeAreaAdmin, self).save_model(request, obj, form, change)
        if form.data.get('add_objs', None):
            try:
                pks = form.data['add_objs'].split('_')
                ct = ContentType.objects.get_for_id(int(pks[0]))
                obj_id = int(pks[1])
                pos = obj.widgets.all().count()
                WidgetInArea.objects.get_or_create(typearea=obj,
                                                   content_type=ct,
                                                   object_id=obj_id,
                                                   position=pos)
            except ValueError, e:
                pass

    def render_change_form(self, request, context, add=False,
                           change=False, form_url='', obj=None):
        if obj:
            clslist = list(itersubclasses(BaseWidget))[:]
            print "clsl", clslist
            context['addable_objs'] = []
            context['addable_widgets'] = []
            found = [c.content_object for c in obj.widgets.all()]
            for c in clslist:
                context['addable_widgets'].append(
                    '<li>+  <a href="%s">%s</a></li>' % (
                    (reverse('admin:%s_%s_add' % (
                        c._meta.app_label, c._meta.module_name)) +
                        "?typearea=%s" % (context['object_id'])
                    ), get_classname(c)
                 ))
                objs = c.objects.all()
                print c, objs
                ctpk = ContentType.objects.get_for_model(c).pk
                for o in objs:
                    if o in found:
                        continue
                    context['addable_objs'].append(
                        '<option  value="%s_%s">o:%s</option>' % (ctpk, o.pk, o,)
                    )
        else:
            self.change_form_template = 'admin/change_form_help_text.html'
            context['help_text'] = '[save] before adding widgets'
        return admin.ModelAdmin.render_change_form(self, request, context,
                                                   add=add, change=change,
                                              form_url=form_url, obj=obj)


class BaseWidgetAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        s = request.GET.get('typearea', None)
        if s:
            ta = TypeArea.objects.get(pk=int(s))
            WidgetInArea.objects.create(
                typearea=ta,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.pk, position=ta.widgets.count())

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
admin.site.register([PageType,  WidgetInArea])
