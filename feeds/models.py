from django.db import models
from django.conf import settings

from common.models import CommonModel


class Feed(CommonModel):

    """
    피드
    """

    content = models.TextField()
    house = models.ForeignKey(
        "houses.Apartment",
        on_delete=models.CASCADE,
        related_name="feeds",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feeds",
    )

    def __str__(self):
        return self.content
