from django.db import models

from common.models import CommonModel


class Apartment(CommonModel):

    """
    300세대 이상 공동주택단지 목록 모델
    """

    address_do = models.CharField(max_length=200, help_text="도")
    address_si = models.CharField(max_length=200, help_text="시군구")
    address_dong = models.CharField(max_length=200, help_text="읍면동")
    address_li = models.CharField(max_length=200, blank=True, help_text="리")
    bjd_code = models.CharField(max_length=200, help_text="법정동코드")
    kapt_code = models.CharField(max_length=200, help_text="단지코드")
    kapt_name = models.CharField(db_index=True, max_length=200, help_text="단지명")

    def __str__(self):
        return (
            self.address_do
            + "  "
            + self.address_si
            + "  "
            + self.address_dong
            + "  "
            + self.kapt_name
        )

    class Meta:
        db_table = "apartment"

        # 위에 보면 kapt_name에도 index 적용 되어 있다.
        indexes = [
            models.Index(fields=["kapt_code"]),
        ]
