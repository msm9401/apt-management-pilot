from django.contrib import admin
from .models import Question, Choice


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "created_at",
        "end_date",
        "remaining_time",
        "status",
        "house",
    )

    list_filter = ("status", "house")

    search_fields = ["house"]

    search_help_text = "주소, 아파트명, 단지코드, 법정동코드 검색"

    autocomplete_fields = ["house"]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):

    list_display = ("question", "title", "votes")

    list_filter = ("question",)

    ordering = ["-votes"]
