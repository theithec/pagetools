from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from pagetools.sections.admin import BasePageNodePosAdmin, BasePageNodeAdmin
from pagetools.sections.models import PageNodePos, PageNode
from .models import Page, Section


class PageNodePosAdmin(BasePageNodePosAdmin):
    model= PageNodePos

class PageNodeAdmin(BasePageNodeAdmin):
    inlines = (PageNodePosAdmin,)
    model = PageNode
    def get22_fieldsets(self, request, obj=None):
        return (
            (_('Meta'), {
                'fields': ('title', 'status',),
            }),
            (_('Translated fields'), {
                'fields': ('headline', 'text',),
            }),
            ('more', {  'fields':('slug','node_type','classes'),
                    'classes': ('grp-collapse grp-closed',),}
            )
        )

class PageAdmin(PageNodeAdmin):
    pass


class SectionAdmin(PageNodeAdmin):
    pass


admin.site.register(PageNode, PageNodeAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
