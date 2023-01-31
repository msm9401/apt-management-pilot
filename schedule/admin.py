from django.contrib import admin
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):

    list_display = ("title", "start_date", "end_date", "house")

    search_fields = ["house__kapt_name"]

    search_help_text = "아파트명 검색"

    autocomplete_fields = ["house"]
