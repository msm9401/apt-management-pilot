from django.contrib import admin
from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):

    list_display = ("title", "created_at", "house")

    list_filter = ("house__address_do",)

    search_fields = ["house"]

    autocomplete_fields = ["house"]
