from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from pagetools.sections.admin import BasePageNodePosAdmin, BasePageNodeAdmin
from pagetools.sections.models import PageNodePos, PageNode
from .models import Page, Section, Article, SectionPage


class PageNodePosAdmin(BasePageNodePosAdmin):
    model = PageNodePos


class PageNodeAdmin(BasePageNodeAdmin):
    inlines = (PageNodePosAdmin,)
    model = PageNode
    change_form_template = 'admin/change_form_chooser.html'

    def get_fieldsets(self, request, obj=None):
        return (
            (_('Meta'), {
                'fields': ('title', 'status',),
            }),
            ('more',
             {
                'fields': ('slug', 'classes'),
                'classes': ('grp-collapse grp-closed', ), })
        )


class SectionPageAdmin(PageNodeAdmin):
    pass


class ArticleAdmin(PageNodeAdmin):

    model = Article

    def get_fieldsets(self, request, obj=None):
        s = super(ArticleAdmin, self).get_fieldsets(request, obj)
        return (s[0],
                ('', {'fields': ('content',)}),
                s[1],)


class SectionAdmin(PageNodeAdmin):

    def get_fieldsets(self, request, obj=None):
        return (super(SectionAdmin, self).get_fieldsets(request, obj)[0],
                ('more', {'fields': ('slug', 'node_type', 'classes'),
                          'classes': ('grp-collapse grp-closed',), }
                ), )


admin.site.register(PageNode, PageNodeAdmin)
admin.site.register(SectionPage, SectionPageAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Section, SectionAdmin)
