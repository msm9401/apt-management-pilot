from rest_framework import serializers

from .models import Comment
from users.serializers import TinyUserSerializer


class CommentDetailSerializer(serializers.ModelSerializer):

    recomment = serializers.SerializerMethodField()
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "content",
            "user",
            "recomment",
            "created_at",
            "updated_at",
        ]

    def get_recomment(self, comment):
        queryset = Comment.objects.filter(parent_comment=comment.id)
        return list(
            queryset.values(
                "id",
                "user__username",
                "user__profile_photo",
                "content",
                "created_at",
                "updated_at",
            )
        )
