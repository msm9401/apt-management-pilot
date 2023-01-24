from rest_framework import serializers

from .models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = [
            "pk",
            "address_do",
            "address_si",
            "address_dong",
            "address_li",
            "kapt_name",
        ]
