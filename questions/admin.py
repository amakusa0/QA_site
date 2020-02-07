from django.contrib import admin
from .models import Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fields = ('title', 'pub_date', 'isSolved', 'text', )
    inlines = [AnswerInline]
    list_display = ('title', 'pub_date',)

admin.site.register(Question, QuestionAdmin)
