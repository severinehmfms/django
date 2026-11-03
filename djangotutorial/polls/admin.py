from django.contrib import admin

from .models import Question
from .models import Choice

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date")
    list_filter = ("pub_date",)
    search_fields = ("question_text",)
    ordering = ("-pub_date",)

# admin.site.register(Question)
admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "choice_text", "votes")
    list_filter = ("question","votes",)
    search_fields = ("choice_text",)
    ordering = ("-question","-votes")

# admin.site.register(Choice)
admin.site.register(Choice, ChoiceAdmin)