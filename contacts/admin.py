from django.contrib import admin
from .models import ContactNumber


@admin.register(ContactNumber)
class ContactsAdmin(admin.ModelAdmin):

    list_display = ("contact_to", "contact_number", "house")

    search_fields = ["house__kapt_name"]

    search_help_text = "아파트명 검색"

    autocomplete_fields = ["house"]
