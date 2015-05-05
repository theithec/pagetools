from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _
from grappelli.forms import GrappelliSortableHiddenMixin

from pagetools.core.admin import PagelikeAdmin
# from .models import Node, Page, Section, Content, Row, NodePos


class BaseNodePosAdmin(GrappelliSortableHiddenMixin, admin.TabularInline):

    def __init__(self, *args, **kwargs):
        super(BaseNodePosAdmin, self).__init__(*args, **kwargs)

    def admin_link(self, instance):
        node = instance.content
        url = reverse('admin:%s_%s_change' % (
            node._meta.app_label,
            self.admin_for.get(node.node_type, node.node_type)),
            args=(node.id,))
        return format_html(u'<a href="{}">Edit</a>', url)
        # … or if you want to include other fields:
        return format_html(u'<a href="{}">Edit: {}</a>', url, instance.title)

    readonly_fields = ('admin_link',)
    fk_name = "group"
    fields = ("content", "position","admin_link",)
    sortable_field_name = "position"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content":
            allowd_children_keys = self.parent_model.allowed_children_keys
            if allowd_children_keys:
                kwargs["queryset"] = self.node_model.public.filter(
                    node_type__in=self.parent_model.allowed_children_keys
                )
        return super(BaseNodePosAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class BaseNodeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseNodeForm, self).__init__(*args, **kwargs)
        if getattr(self.instance,  'node_type_keys', False):
            self.fields['node_type'].choices = [
                #gc for gc in Node.group_choices
                gc for gc in self._meta.model.group_choices
                if gc[0] in self.instance.node_type_keys
            ]

    class Meta:
        #model = Node
        exclude = ('',)


#class NodeAdmin(TranslatableAdmin,PagelikeAdmin ):
class BaseNodeAdmin(PagelikeAdmin ):
    inlines = (BaseNodePosAdmin,)
    # model = Node
    # form = NodeForm
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('status_changed',)

    list_display=('title', 'node_type','lang', 'status', 'status_changed')
    list_filter=('node_type','lang', 'status')
    search_fields = ('title',)

    def get_queryset(self, request):
        qs = super(BaseNodeAdmin, self).get_queryset(request)
        if getattr(self.model,  'node_type_keys', False):
            return qs.filter(node_type__in=self.model.node_type_keys)
        return qs
    #def response_change(self, request, obj):
    #    return super(TranslatableAdmin, self).response_change(request, obj)

title_fieldsets = (
        ('Meta', {'fields':( 'headline',  'status', 'lang','status_changed')}),
        ('more', {  'fields':('slug','node_type'),
                    'classes': ('grp-collapse grp-closed',),}
        ),
    )
_fields = ('title', 'headline',  'text','status', 'lang','status_changed')




