from django.db import models

from common.models import CommonModel


class ContactNumber(CommonModel):

    """
    연락처
    """

    contact_to = models.CharField(max_length=140)  # 연락처 대상(관리사무소, 특정인물 등등)
    contact_number = models.CharField(max_length=30)  # 전화번호
    house = models.ForeignKey(
        "houses.Apartment",
        on_delete=models.CASCADE,
        related_name="contacts",
    )

    def __str__(self):
        return self.contact_to

    class Meta:
        db_table = "contact"
