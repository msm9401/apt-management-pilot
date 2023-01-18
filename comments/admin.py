from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ("content", "user", "feed", "parent_comment")

    list_filter = ("user", "feed")

    search_fields = ["user"]

    raw_id_fields = ["feed", "user"]
