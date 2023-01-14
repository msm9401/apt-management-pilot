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

    list_filter = ("user", "current_status", "house")

    search_fields = ["house"]

    autocomplete_fields = ["house"]
