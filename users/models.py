from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.core.validators import RegexValidator


class ComfirmedUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_confirmed=True)


class UnconfirmedUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_confirmed=False)


class User(AbstractUser):
    phoneNumberRegex = RegexValidator(
        regex=r"^01([0|1|6|7|8|9]?)([0-9]{3,4})([0-9]{4})$"
    )

    name = models.CharField(max_length=30, blank=True, help_text="이름(실명)")
    first_name = None
    last_name = None
    profile_photo = models.URLField(blank=True, help_text="유저 프로필 이미지")
    phone_number = models.CharField(
        validators=[phoneNumberRegex],
        max_length=11,
        unique=True,
        blank=True,
        null=True,
        help_text="전화번호",
    )
    my_houses = models.ManyToManyField(
        "houses.Apartment", blank=True, related_name="users"
    )
    apt_number = models.CharField(max_length=30, blank=True, help_text="아파트 동")
    house_number = models.CharField(max_length=30, blank=True, help_text="아파트 호수")
    is_confirmed = models.BooleanField(default=False, help_text="주민 확인 여부")

    objects = UserManager()
    confirmed = ComfirmedUserManager()
    unconfirmed = UnconfirmedUserManager()

    class Meta:
        default_manager_name = "objects"
