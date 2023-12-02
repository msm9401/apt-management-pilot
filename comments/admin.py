from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "user", "feed", "parent_comment")

    list_filter = ("created_at",)

    search_fields = ["user"]

    raw_id_fields = ["feed", "user"]

    # list_select_related = True
    # list_dispaly에 무엇을 표시하는냐에 따라 최적화 직접 해줘야 한다.
    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("comments", "feed")
            .select_related("parent_comment", "user")
        )
