from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #  fields = ['pub_date', 'question_text']
    fieldsets = (
        ('', {'fields': ['pub_date', 'question_text']}),
    )
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

