from rest_framework.serializers import ModelSerializer

from .models import Question


class QuestionListSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "pk",
            "created_at",
            "title",
            "end_date",
        ]


class QuestionDetailSerializer(ModelSerializer):
    class Meta:
        model = Question
        exclude = ["house"]
