from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from django.contrib.contenttypes.models import ContentType
from grappelli.forms import GrappelliSortableHiddenMixin
from pagetools.core.admin import PagelikeAdmin
from pagetools.core.utils import importer
from pagetools.menus.admin import EntrieableAdmin
from .models import PageNode, PageNodePos


class BasePageNodePosAdmin(GrappelliSortableHiddenMixin, admin.TabularInline):

    model = PageNodePos
    readonly_fields = ('admin_link',)
    fk_name = "owner"
    sortable_field_name = "position"
    extra = 1

    def get_queryset(self, request):
        print("\nGETQS", self)
        request.parent_model = self.parent_model
        qs = super(
            BasePageNodePosAdmin, self
        ).get_queryset(request).prefetch_related(
            'content__content_object').order_by('content__title')
        print("\nENDQS\n")
        return qs

    # TODO To utils (see dashboardmodul)
    def admin_link(self, instance):
        realobj = instance.content.content_object #get_real_obj()
        url = reverse('admin:%s_%s_change' % (realobj._meta.app_label,
                                              realobj._meta.model_name),
                      args=(realobj.id,))
        return format_html(u'<a href="{}">Edit</a>', url)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        #if db_field.name == "content" and getattr(
        #    self.parent_model, 'allowed_children_classes', False
        #):
        if db_field.name == "content":
            print("get content")
            kwargs["queryset"] = self.content_queryset
            return super(BasePageNodePosAdmin, self).formfield_for_foreignkey(
                db_field, request, **kwargs
            )


class BasePageNodeAdmin(PagelikeAdmin):

    #inlines = [BasePageNodePosAdmin]
    change_form_template = 'admin/change_form_chooser.html'

    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('status_changed', 'containing_nodes')


    def admin_link(self, instance):
        realobj = instance.content_object # get_real_obj()
        url = reverse('admin:%s_%s_change' % (realobj._meta.app_label,
                                              realobj._meta.model_name),
                      args=(realobj.id,))
        return format_html(u'<a href="{}">{}</a>', url, realobj)
    admin_link.short_description = _("Admin link")

    def get_queryset(self, request):
        #real_pk = self.model.get_contenttype_pk()
        #iqs = self.model._default_manager.filter(content_type_pk=real_pk)

        allowed_children_classes = self.model.allowed_children_classes
        print("ALLOWED", [(type(a),a) for a in allowed_children_classes])

        allowed_contenttypes = [
            ContentType.objects.get_for_model(
                importer(acc), for_concrete_model=False).pk
            for acc in allowed_children_classes
        ]

        print("GETPANENODEQS")
        BasePageNodePosAdmin.content_queryset = PageNode.objects.filter(
            content_type_pk__in=allowed_contenttypes
        ).order_by('title')
        list(BasePageNodePosAdmin.content_queryset) # = PageNode.objects.filter(

        qs = self.model.objects.all().prefetch_related('content_object') #ifilter(content_type_pk=real_pk)
        return qs

    def containing_nodes(self, instance):
        parents = instance.in_nodes.all()
        txt = ", ".join([self.admin_link(p) for p in parents])
        return txt
    containing_nodes.short_description = _("Parents")
    containing_nodes.allow_tags = _("Parents")


admin.site.register(PageNode)


'''
@admin.register(SimpleArticle)
class SimpleArticleAdmin(BasePageNodeAdmin):
    inlines = [BasePageNodePosAdmin]
    fieldsets = (
        ('', {'fields': [
            'status',
            'title',
            'slug',
            'content',
            'containing_nodes',
        ]}),
        (_('Teaser'), {'fields': ['teaser', ]}),
    )
    readonly_fields = ('status_changed','containing_nodes')


@admin.register(SimpleSection)
class SimpleSectionAdmin(BasePageNodeAdmin):
    inlines = [BasePageNodePosAdmin]
    fieldsets = (
        ('', {'fields': [
            'status',
            'title',
            'slug',
            'containing_nodes',
        ]}),
    )
    readonly_fields = ('status_changed','containing_nodes')

@admin.register(SimpleSectionPage)
class SimplePageAdmin(EntrieableAdmin, BasePageNodeAdmin):
    inlines = [BasePageNodePosAdmin]
    fieldsets = (
        ('', {'fields': [
            'status',
            'title',
            'slug',
            'description',
        ]}),
        ('', {'fields': ['menus']}),
    )

'''
