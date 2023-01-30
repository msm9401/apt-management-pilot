from django.shortcuts import get_list_or_404

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
        queryset = ContactNumber.objects.filter(
            house__kapt_name=self.kwargs["kapt_name"]
        )
        return get_list_or_404(queryset)

    def perform_create(self, serializer):
        serializer.save(house=Apartment.objects.get(kapt_name=self.kwargs["kapt_name"]))


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ContactDetailSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = ContactNumber.objects.filter(
            house__kapt_name=self.kwargs["kapt_name"],
            pk=self.kwargs["pk"],
        )
        return queryset
