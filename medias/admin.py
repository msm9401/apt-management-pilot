from django.contrib import admin

from .models import Photo, Video


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):

    list_display = ("file", "feed", "complaint", "poll", "notice", "user", "house")

    list_filter = ("user", "feed", "complaint", "poll", "notice")

    search_fields = ["house"]

    search_help_text = "주소, 아파트명, 단지코드, 법정동코드 검색"

    raw_id_fields = ["user", "house", "feed", "complaint", "poll", "notice"]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):

    list_display = ("file", "feed", "complaint", "notice", "user", "house")

    list_filter = ("user", "feed", "complaint", "notice")

    search_fields = ["house"]

    search_help_text = "주소, 아파트명, 단지코드, 법정동코드 검색"

    raw_id_fields = ["user", "house", "feed", "complaint", "notice"]
