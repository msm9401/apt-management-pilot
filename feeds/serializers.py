from rest_framework import serializers

from medias.serializers import PhotoSerializer
from .models import Feed
from comments.models import Comment


class FeedListSerializer(serializers.ModelSerializer):

    photos = PhotoSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = "__all__"

    def get_comments_count(self, feed):
        return feed.comments.count()


class FeedDetailSerializer(serializers.ModelSerializer):

    photos = PhotoSerializer(many=True, read_only=True)
    excluded_recomments = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = "__all__"

    def get_excluded_recomments(self, feed):

        """
        대댓글을 제외한 피드의 댓글만 가져오는 함수
        """

        queryset = Comment.objects.filter(feed_id=feed.pk) & Comment.objects.filter(
            parent_comment=None
        )
        return list(queryset.values())
