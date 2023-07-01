from django.db.models import Count

from rest_framework import serializers

from medias.serializers import PhotoSerializer
from users.serializers import TinyUserSerializer
from comments.models import Comment
from .models import Feed


class FeedListSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Feed
        exclude = ["house"]

    def get_comments_count(self, feed):
        return feed.comments.count()


class FeedDetailSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    user = TinyUserSerializer(read_only=True)
    only_comments = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        exclude = ["house"]

    # 대댓글을 제외한 피드의 댓글만 가져오는 함수(대댓글은 개수만 표시)
    def get_only_comments(self, feed):
        queryset = Comment.objects.filter(feed_id=feed.pk, parent_comment=None)
        return list(
            queryset.values(
                "id",
                "created_at",
                "updated_at",
                "content",
                "user__username",
                "user__profile_photo",
            ).annotate(recomment_count=Count("comments"))
        )
