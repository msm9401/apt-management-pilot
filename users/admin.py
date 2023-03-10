from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):

    fieldsets = (
        (
            "profile",
            {
                "fields": (
                    "username",
                    "password",
                    "name",
                    "email",
                    "phone_number",
                    "my_houses",
                    "apt_number",
                    "house_number",
                    "profile_photo",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("username", "name", "phone_number", "apt_number", "house_number")

    autocomplete_fields = ["my_houses"]
