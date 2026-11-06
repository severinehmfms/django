from django.contrib import admin

from .models import Question
from .models import Choice

class QuestionAdmin(admin.ModelAdmin):
    # Champs qui seront affichés dans la liste
    list_display = ("question_text", "pub_date")
    # Champs sur lesquels on pourra filtrer
    list_filter = ("pub_date",)
    # Champs pour la recherche
    search_fields = ("question_text",)
    # Ordre (décroissant de date)
    ordering = ("-pub_date",)

    # Pour ordonner les champs (c'est l'un ou l'autre soit fields soit fieldset)
    # fields = ["pub_date", "question_text"]

    # Partager le formulaire en plusieurs sous-ensembles (fieldsets)
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]

# admin.site.register(Question)
admin.site.register(Question, QuestionAdmin)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "choice_text", "votes")
    list_filter = ("question","votes",)
    search_fields = ("choice_text",)
    ordering = ("-question","-votes")

# admin.site.register(Choice)
admin.site.register(Choice, ChoiceAdmin)
