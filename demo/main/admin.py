from django.contrib import admin

from pagetools.sections.admin import BasePageNodeAdmin

from pagetools.menus.admin import EntrieableAdmin, EntrieableForm

from .models import Article, Section, SectionList, ChoosableTemplateWidget

# @admin.register(SectionList)
class MainSectionsAdmin(BasePageNodeAdmin,EntrieableAdmin):
    form = EntrieableForm
    exclude =  ['content_type_pk', 'object_id',]

admin.site.register([Article, Section, SectionList], MainSectionsAdmin)
admin.site.register(ChoosableTemplateWidget)



# Register your models here.
