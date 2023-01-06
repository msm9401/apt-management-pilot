from django.contrib import admin
from .models import Question, Choice


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):

    list_display = ("question", "title", "votes")

    list_filter = ("question",)
