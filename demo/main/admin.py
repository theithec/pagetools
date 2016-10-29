from django.contrib import admin

from pagetools.sections.admin import BasePageNodeAdmin

from pagetools.menus.admin import EntrieableAdmin, EntrieableForm

from .models import Article, Section, SectionList

@admin.register(SectionList)
class SectionListAdmin(BasePageNodeAdmin,EntrieableAdmin ):
    form = EntrieableForm
    pass

admin.site.register([Article, Section, ], BasePageNodeAdmin)



# Register your models here.
