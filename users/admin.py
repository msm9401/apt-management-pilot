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
                    "is_confirmed",
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

    list_display = (
        "username",
        "name",
        "phone_number",
        "apt_number",
        "house_number",
        "is_confirmed",
    )

    list_filter = ("is_confirmed", "apt_number")

    search_fields = ["username", "name", "phone_number"]

    search_help_text = "유저 아이디, 실명, 전화번호 검색"

    autocomplete_fields = ["my_houses"]

    def get_queryset(self, request):
        """
        관리자 아파트의 유저만 get.
        superuser(웹마스터)는 아파트에 관계없이 모든 유저 get.
        """
        if not request.user.is_superuser:
            return (
                super()
                .get_queryset(request)
                .filter(my_houses=request.user.my_houses.first())
            )

        return super().get_queryset(request)
