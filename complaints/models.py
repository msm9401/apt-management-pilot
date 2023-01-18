from django.db import models
from django.conf import settings

from common.models import CommonModel


class Complaint(CommonModel):

    """
    민원접수
    """

    title = models.CharField(max_length=150)
    description = models.TextField()
    current_status = models.BooleanField(default=False)  # 민원 해결 상태
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="complaints",
    )
    house = models.ForeignKey(
        "houses.Apartment",
        on_delete=models.CASCADE,
        related_name="complaints",
    )

    def __str__(self):
        return self.title
