from django.db import models
from common.models import CommonModel


class Notice(CommonModel):

    """
    아파트 공지사항
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    house = models.ForeignKey(
        "houses.Apartment",
        on_delete=models.CASCADE,
        related_name="notices",
    )

    def __str__(self):
        return self.title
