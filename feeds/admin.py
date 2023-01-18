from django.contrib import admin

from .models import Feed


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):

    list_display = ("content", "house", "user")

    list_filter = ("house",)

    search_fields = ["house"]

    search_help_text = "주소, 아파트명, 단지코드, 법정동코드 검색"

    raw_id_fields = ["house", "user"]
