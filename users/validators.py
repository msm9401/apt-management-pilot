from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r"^01([0|1|6|7|8|9])([0-9]{3,4})([0-9]{4})$"
    message = _("The phone number format is not correct.")
