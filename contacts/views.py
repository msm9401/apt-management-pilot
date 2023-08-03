from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import ContactNumber
from .serializers import ContactListSerializer, ContactDetailSerializer
from houses.models import Apartment
from common.permissions import IsAdminUserOrAuthenticatedReadOnly


class ContactListCreate(generics.ListCreateAPIView):
    serializer_class = ContactListSerializer
    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        queryset = ContactNumber.objects.filter(house__kapt_code=kapt_code)
        return queryset

    def perform_create(self, serializer):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        serializer.save(house=Apartment.objects.get(kapt_code=kapt_code))


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactDetailSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        queryset = ContactNumber.objects.filter(
            house__kapt_code=kapt_code,
            pk=self.kwargs["pk"],
        )
        return queryset
