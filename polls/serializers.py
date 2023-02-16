from rest_framework import serializers

from .models import Question, Choice


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "pk",
            "created_at",
            "title",
            "end_date",
        ]


class QuestionDetailSerializer(serializers.ModelSerializer):

    choice_list = serializers.SerializerMethodField()

    class Meta:
        model = Question
        exclude = ["house"]

    def get_choice_list(self, question):
        return Choice.objects.filter(question=question.id).values(
            "title",
            "description",
            "votes",
        )
