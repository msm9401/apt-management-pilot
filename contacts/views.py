from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied

from .models import ContactNumber
from .serializers import ContactListSerializer, ContactDetailSerializer
from houses.models import Apartment
from common.permissions import IsAdminUserOrAuthenticatedReadOnly


class ContactListCreate(generics.ListCreateAPIView):

    serializer_class = ContactListSerializer
    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        my_apt = self.request.user.my_houses.filter(kapt_name=self.kwargs["kapt_name"])
        if my_apt:
            queryset = ContactNumber.objects.filter(house=my_apt[0])
            return queryset
        raise PermissionDenied

    def perform_create(self, serializer):
        serializer.save(house=Apartment.objects.get(kapt_name=self.kwargs["kapt_name"]))


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ContactDetailSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.my_houses.filter(
            kapt_name=self.kwargs["kapt_name"]
        ).exists():
            queryset = ContactNumber.objects.filter(
                house__kapt_name=self.kwargs["kapt_name"],
                pk=self.kwargs["pk"],
            )
            return queryset
        raise PermissionDenied
