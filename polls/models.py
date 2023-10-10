import datetime

from django.db import models
from common.models import CommonModel


class Question(CommonModel):

    """
    설문조사 주제
    """

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)
    house = models.ForeignKey(
        "houses.Apartment",
        on_delete=models.CASCADE,
        related_name="polls",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "question"
        ordering = ["-created_at"]


class Choice(CommonModel):

    """
    설문조사 주제에 대한 선택지
    """

    question = models.ForeignKey(
        "polls.Question",
        on_delete=models.CASCADE,
        related_name="choices",
    )
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "choice"
        ordering = ["created_at"]
