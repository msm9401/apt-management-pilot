from django.contrib import admin
from django.conf import settings
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "user",
        "created_at",
        "current_status",
        "house",
    )

    list_filter = ("current_status",)

    search_fields = ["house__kapt_name"]

    search_help_text = "아파트명 검색"

    autocomplete_fields = ["house"]
