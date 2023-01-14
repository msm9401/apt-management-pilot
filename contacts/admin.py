from django.contrib import admin
from .models import ContactNumber


@admin.register(ContactNumber)
class ContactsAdmin(admin.ModelAdmin):

    list_display = ("contact_to", "contact_number", "house")

    search_fields = ["house"]

    autocomplete_fields = ["house"]
