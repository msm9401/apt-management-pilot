from rest_framework import serializers

from .models import Complaint
from users.serializers import TinyUserSerializer


class ComplaintListSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Complaint
        fields = [
            "pk",
            "user",
            "title",
            "current_status",
        ]
        read_only_fields = ["current_status"]


class ComplaintCreateSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Complaint
        exclude = ["house", "current_status"]


class ComplaintDetailSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Complaint
        exclude = ["house"]
