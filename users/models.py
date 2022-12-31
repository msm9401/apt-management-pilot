from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):

    """
    User Model Definition
    """

    phoneNumberRegex = RegexValidator(
        regex=r"^01([0|1|6|7|8|9]?)([0-9]{3,4})([0-9]{4})$"
    )

    name = models.CharField(
        max_length=30,
        default="관리자",
        help_text="이름",
    )
    phone_number = models.CharField(
        validators=[phoneNumberRegex],
        max_length=11,
        unique=True,
        default="11111111111",
        help_text="전화번호",
    )
    apt_number = models.PositiveSmallIntegerField(default=1, help_text="아파트 동")
    house_number = models.PositiveSmallIntegerField(default=1, help_text="아파트 호수")
