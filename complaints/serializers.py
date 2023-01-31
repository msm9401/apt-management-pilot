from rest_framework.serializers import ModelSerializer

from .models import Complaint
from users.serializers import TinyUserSerializer


class ComplaintListSerializer(ModelSerializer):

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


class ComplaintCreateSerializer(ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Complaint
        exclude = ["house", "current_status"]


class ComplaintDetailSerializer(ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Complaint
        exclude = ["house"]
