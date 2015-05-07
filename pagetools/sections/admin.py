from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from grappelli.forms import GrappelliSortableHiddenMixin


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
                                            admin_for.get(node.node_type, node.node_type)),
                                            #node._meta.module_name),
                    args=(node.id,))
        return format_html(u'<a href="{}">Edit</a>', url)
        # … or if you want to include other fields:
        return format_html(u'<a href="{}">Edit: {}</a>', url, instance.title)

    #readonly_fields = ('admin_link',)
    fk_name = "owner"
    fields = ("content","position",) #admin_link",)
    sortable_field_name = "position"

    def formfield_for_foreignkey2(self, db_field, request, **kwargs):
        print ("PM", self.parent_model)
        #print("PP", self.instance)
        if db_field.name == "content":
            allowed_children_keys = self.parent_model.allowed_children_keys
            print ("ALLC", allowed_children_keys)
            if allowed_children_keys:
                kwargs["queryset"] = self.parent_model.public.filter(
                    node_type__in=allowed_children_keys
                )
        return super(BasePageNodePosAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )



class BasePageNodeAdmin(admin.ModelAdmin):
    pass
    #model = NodePos


