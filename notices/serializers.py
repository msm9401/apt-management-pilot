from rest_framework import serializers

from .models import Notice


class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            "pk",
            "title",
            "created_at",
        ]


class NoticeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        exclude = ["house"]
