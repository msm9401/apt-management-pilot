from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Question, Choice


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

    choice_list = SerializerMethodField()

    class Meta:
        model = Question
        exclude = ["house"]

    def get_choice_list(self, question):
        return Choice.objects.filter(question=question.id).values(
            "title",
            "description",
            "votes",
        )
