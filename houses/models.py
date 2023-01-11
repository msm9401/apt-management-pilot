from django.db import models
from common.models import CommonModel


class Apartment(CommonModel):

    """
    300세대 이상 공동주택단지 목록 모델
    나중에 필드이름 바꾸자. 아무생각 없이 api로 추출한 dict의 key값으로 만들어놓음.
    """

    as1 = models.CharField(max_length=200)  # 시도
    as2 = models.CharField(max_length=200)  # 시군구
    as3 = models.CharField(max_length=200)  # 읍면동
    as4 = models.CharField(max_length=200, null=True, blank=True)  # 리
    bjdCode = models.CharField(max_length=200)  # 법정동코드
    kaptCode = models.CharField(max_length=200)  # 단지코드
    kaptName = models.CharField(max_length=200)  # 단지명

    def __str__(self):
        return self.kaptName
