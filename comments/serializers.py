from datetime import timedelta

from django.db.models import Q, F
from django.db.models.functions import TruncDate

from rest_framework import serializers

from .models import Comment
from users.serializers import TinyUserSerializer


class CommentDetailSerializer(serializers.ModelSerializer):
    recomments = serializers.SerializerMethodField()
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "content",
            "user",
            "recomments",
            "created_at_string",
            "updated_at_string",
        ]

    def get_recomments(self, comment):
        # queryset = Comment.objects.filter(parent_comment=comment.id)

        # 대댓글에도 답글달 수 있게 변경 후 답글도 불러올 수 있도록 변경
        # 해당 피드의 parent_comment가 null이 아니면 불러오는 쿼리셋(임시)
        queryset = Comment.objects.filter(
            Q(feed=comment.feed) & Q(parent_comment__isnull=False)
        )

        return list(
            queryset.values(
                "id",
                "user__username",
                "user__profile_photo",
                "content",
                # "created_at",
                # "updated_at",
            ).annotate(
                # created_at_string=F("created_at") + timedelta(hours=9),
                # updated_at_string=F("updated_at") + timedelta(hours=9),
                created_at_string=TruncDate(F("created_at")),
                updated_at_string=TruncDate(F("updated_at")),
            )
        )
