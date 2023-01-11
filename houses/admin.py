from django.contrib import admin
from .models import Apartment


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):

    list_display = ("as1", "as2", "as3", "as4", "bjdCode", "kaptCode", "kaptName")

    list_filter = ("as1", "as2", "as3", "as4")

    list_max_show_all = 5

    list_per_page = 50

    search_fields = ["as1", "as2", "as3", "as4", "bjdCode", "kaptCode", "kaptName"]

    search_help_text = "주소, 아파트명, 단지코드, 법정동코드 검색"
