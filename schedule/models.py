from django.db import models
from common.models import CommonModel


class Schedule(CommonModel):

    """
    일정표
    """

    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    house = models.ForeignKey(
        "houses.Apartment",
        on_delete=models.CASCADE,
        related_name="schedule",
    )

    def __str__(self):
        return self.title
