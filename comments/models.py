from django.db import models
from django.conf import settings

from common.models import CommonModel


class Comment(CommonModel):

    """
    댓글, 대댓글
    """

    content = models.CharField(max_length=500)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.content
