from django.db import models
from common.models import CommonModel


class Apartment(CommonModel):

    """
    300세대 이상 공동주택단지 목록 모델
    """

    address_do = models.CharField(max_length=200)  # 도
    address_si = models.CharField(max_length=200)  # 시군구
    address_dong = models.CharField(max_length=200)  # 읍면동
    address_li = models.CharField(max_length=200, blank=True)  # 리
    bjd_code = models.CharField(max_length=200)  # 법정동코드
    kapt_code = models.CharField(max_length=200)  # 단지코드
    kapt_name = models.CharField(max_length=200)  # 단지명

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
