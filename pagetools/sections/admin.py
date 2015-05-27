from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from django.contrib.contenttypes.models import ContentType
from grappelli.forms import GrappelliSortableHiddenMixin
from pagetools.core.admin import PagelikeAdmin
from .models import PageNode, PageNodePos


class BasePageNodePosAdmin(GrappelliSortableHiddenMixin, admin.TabularInline):

    model = PageNodePos
    readonly_fields = ('admin_link',)
    fk_name = "owner"
    sortable_field_name = "position"

    def get_queryset(self, request):
        request.parent_model = self.parent_model
        return super(BasePageNodePosAdmin, self).get_queryset(request)

    def admin_link(self, instance):
        realobj = instance.content.get_real_obj()
        url = reverse('admin:%s_%s_change' % (realobj._meta.app_label,
                                              realobj._meta.model_name),
                      args=(realobj.id,))
        return format_html(u'<a href="{}">Edit</a>', url)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content" and  getattr(
            self.parent_model, 'allowed_children_classes', False
        ):
            allowed_children_classes = self.parent_model.allowed_children_classes
            allowed_contenttypes = [
                ContentType.objects.get_for_model(acc,for_concrete_model=False).pk
                for acc in allowed_children_classes
            ]

            kwargs["queryset"] = PageNode.objects.filter(
                content_type_pk__in=allowed_contenttypes
            )
            return super(BasePageNodePosAdmin, self).formfield_for_foreignkey(
                db_field, request, **kwargs
            )


class BasePageNodeAdmin(PagelikeAdmin):

    def get_queryset(self, request):
        return self.model.objects.real(request=request)

    def admin_link(self, instance):
        realobj = instance.get_real_obj()
        url = reverse('admin:%s_%s_change' % (realobj._meta.app_label,
                                              realobj._meta.model_name),
                      args=(realobj.id,))
        return format_html(u'<a href="{}">{}</a>', url, realobj)
    admin_link.short_description = _("Admin link")

    def containing_nodes(self, instance):
        parents = instance.in_nodes.all()
        txt = ", ".join([self.admin_link(p) for p in  parents])
        return txt
    containing_nodes.short_description = _("Parents")





