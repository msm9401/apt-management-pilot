from django.contrib import admin
from .models import Apartment


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):

    list_display = (
        "address_do",
        "address_si",
        "address_dong",
        "address_li",
        "bjd_code",
        "kapt_code",
        "kapt_name",
    )

    list_filter = ("address_do", "address_si", "address_dong", "address_li")

    list_max_show_all = 5

    list_per_page = 50

    search_fields = [
        "address_do",
        "address_si",
        "address_dong",
        "address_li",
        "bjd_code",
        "kapt_code",
        "kapt_name",
    ]

    search_help_text = "주소, 아파트명, 단지코드, 법정동코드 검색"
