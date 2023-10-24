from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Feed


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ("content", "house", "link_to_user")

    list_filter = ("created_at",)

    search_fields = ["house__kapt_name", "user__username"]

    search_help_text = "아파트명 검색, 사용자 아이디 검색"

    raw_id_fields = ["house", "user"]

    def get_queryset(self, request):
        """
        관리자 아파트의 피드만 get.
        superuser(웹마스터)는 아파트에 관계없이 모든 피드 get.
        """
        if not request.user.is_superuser:
            return (
                super()
                .get_queryset(request)
                .filter(house=request.user.my_houses.first())
            )

        return super().get_queryset(request)

    @admin.display(description="user")
    def link_to_user(self, object):
        link = reverse("admin:users_user_change", args=[object.user.id])
        return format_html('<a href="{}">🔗{}</a>', link, object.user)
