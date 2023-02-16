from rest_framework import serializers

from .models import ContactNumber


class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactNumber
        fields = [
            "pk",
            "contact_to",
            "contact_number",
        ]


class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactNumber
        exclude = ["house"]
