from rest_framework.serializers import ModelSerializer

from .models import Schedule


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            "pk",
            "title",
            "start_date",
            "end_date",
        ]
