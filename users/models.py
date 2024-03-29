from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.core.validators import RegexValidator

from rest_framework.exceptions import PermissionDenied

from .validators import PhoneNumberValidator


class ComfirmedUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_confirmed=True)


class UnconfirmedUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_confirmed=False)


class User(AbstractUser):
    first_name = None
    last_name = None

    name = models.CharField(
        max_length=30,
        blank=True,
        help_text="이름(실명)",
        verbose_name="이름",
    )
    profile_photo = models.FileField(
        blank=True,
        help_text="유저 프로필 이미지",
        verbose_name="프로필 이미지",
    )
    phone_number = models.CharField(
        validators=[PhoneNumberValidator()],
        max_length=11,
        unique=True,
        blank=True,
        null=True,
        help_text="전화번호",
        verbose_name="전화번호",
    )
    my_houses = models.ManyToManyField(
        "houses.Apartment",
        blank=True,
        related_name="users",
        verbose_name="유저 아파트",
    )
    apt_number = models.CharField(
        max_length=30,
        blank=True,
        help_text="아파트 동",
        verbose_name="아파트 동",
    )
    house_number = models.CharField(
        max_length=30,
        blank=True,
        help_text="아파트 호수",
        verbose_name="아파트 호수",
    )
    is_confirmed = models.BooleanField(
        default=False,
        help_text="주민 확인 여부",
        verbose_name="주민 확인 여부",
    )

    objects = UserManager()
    confirmed = ComfirmedUserManager()
    unconfirmed = UnconfirmedUserManager()

    # 요청하는 유저의 본인 집인지 검증(아파트명이 같은 경우가 있으므로 단지코드로 반환)
    def check_my_house(self, **kwargs):
        if not self.my_houses.filter(**kwargs).exists():
            raise PermissionDenied
        house = self.my_houses.filter(**kwargs)[0]
        return house.kapt_code

    class Meta:
        db_table = "user"
        default_manager_name = "objects"
        verbose_name = "주민"
        verbose_name_plural = "주민"
