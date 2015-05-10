from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from django.contrib.contenttypes.models import ContentType
from grappelli.forms import GrappelliSortableHiddenMixin
from .models import PageNode

class BasePageNodePosAdmin(GrappelliSortableHiddenMixin, admin.TabularInline):

    def __init__(self, *args, **kwargs):
        super(BasePageNodePosAdmin, self).__init__(*args, **kwargs)

    def admin_link2(self, instance):
        admin_for = {
            'slider': 'row',
            'angular-icons': 'row',
            'product': 'content',
            'product-slider': 'content',
        }
        node = instance.content
        url = reverse('admin:%s_%s_change' % (node._meta.app_label,
                                              admin_for.get(
                                                  node.node_type,
                                                  node.node_type)
                                             ),
                                             args=(node.id,))
        return format_html(u'<a href="{}">Edit</a>', url)
    # … or if you want to include other fields:
    # return format_html(u'<a href="{}">Edit: {}</a>', url, instance.title)

    # readonly_fields = ('admin_link',)
    fk_name = "owner"
    #fields = ("content", "position",)
    sortable_field_name = "position"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content" and  getattr(
            self.parent_model, 'allowed_children_classes', False
        ):
            allowed_children_classes = self.parent_model.allowed_children_classes
            allowed_contenttypes = [
                ContentType.objects.get_for_model(acc,for_concrete_model=False).pk
                for acc in allowed_children_classes
            ]

            #if allowed_children_keys:
            #kwargs["queryset"] = self.parent_model.objects.filter(
            kwargs["queryset"] = PageNode.objects.filter(
                #content_type_pk__in=allowed_contenttypes
                content_type_pk__in=allowed_contenttypes
            )
        return super(BasePageNodePosAdmin, self).formfield_for_foreignkey(
                db_field, request, **kwargs
            )



class BasePageNodeAdmin(admin.ModelAdmin):
    pass
#model = NodePos


