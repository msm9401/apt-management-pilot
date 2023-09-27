from rest_framework import serializers

from .models import Question, Choice


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "pk",
            "created_at_string",
            "title",
            "end_date",
        ]


class QuestionDetailSerializer(serializers.ModelSerializer):
    choice_list = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id",
            "choice_list",
            "created_at_string",
            "title",
            "description",
            "end_date",
            "status",
        ]

    def get_choice_list(self, question):
        return Choice.objects.filter(question=question.id).values(
            "title",
            "description",
            "votes",
        )
