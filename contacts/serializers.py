from rest_framework.serializers import ModelSerializer

from .models import ContactNumber


class ContactListSerializer(ModelSerializer):
    class Meta:
        model = ContactNumber
        fields = [
            "pk",
            "contact_to",
            "contact_number",
        ]


class ContactDetailSerializer(ModelSerializer):
    class Meta:
        model = ContactNumber
        exclude = ["house"]
