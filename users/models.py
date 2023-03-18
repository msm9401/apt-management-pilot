from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):

    phoneNumberRegex = RegexValidator(
        regex=r"^01([0|1|6|7|8|9]?)([0-9]{3,4})([0-9]{4})$"
    )

    name = models.CharField(
        max_length=30,
        blank=True,
        help_text="이름",
    )
    first_name = None
    last_name = None
    profile_photo = models.URLField(blank=True)
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
