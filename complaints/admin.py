from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "description",
        "user",
        "created_at",
        "current_status",
    )

    list_filter = (
        "user",
        "current_status",
    )
