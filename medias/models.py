from django.db import models
from django.conf import settings

from common.models import CommonModel


class Photo(CommonModel):

    """
    피드, 민원접수, 투표, 공지사항 중 하나에 속하는 사진
    """

    file = models.URLField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    house = models.ForeignKey(
        "houses.Apartment",
        on_delete=models.CASCADE,
        related_name="photos",
    )
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    complaint = models.ForeignKey(
        "complaints.Complaint",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    notice = models.ForeignKey(
        "notices.Notice",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    poll = models.ForeignKey(
        "polls.Question",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self):
        return "Photo File"


class Video(CommonModel):

    """
    피드, 민원접수, 공지사항 중 하나에 속하는 동영상
    """

    file = models.URLField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="videos",
    )
    house = models.ForeignKey(
        "houses.Apartment",
        on_delete=models.CASCADE,
        related_name="videos",
    )
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="videos",
    )
    complaint = models.ForeignKey(
        "complaints.Complaint",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="videos",
    )
    notice = models.ForeignKey(
        "notices.Notice",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="videos",
    )

    def __str__(self):
        return "Video File"
