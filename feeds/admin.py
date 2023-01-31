from django.contrib import admin

from .models import Feed


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):

    list_display = ("content", "house", "user")

    list_filter = ("house",)

    search_fields = ["house__kapt_name"]

    search_help_text = "아파트명 검색"

    raw_id_fields = ["house", "user"]
