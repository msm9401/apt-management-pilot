from django.shortcuts import get_list_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Complaint
from .serializers import (
    ComplaintListSerializer,
    ComplaintCreateSerializer,
    ComplaintDetailSerializer,
)
from houses.models import Apartment
from common.permissions import IsAdminUserOrAuthenticatedReadOnly


class ComplaintListCreate(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        my_apt = self.request.user.my_houses.filter(kapt_name=self.kwargs["kapt_name"])
        if my_apt:
            queryset = Complaint.objects.filter(house=my_apt[0]).select_related("user")
            return queryset
        raise PermissionDenied

    def perform_create(self, serializer):
        serializer.save(
            house=Apartment.objects.get(kapt_name=self.kwargs["kapt_name"]),
            user=self.request.user,
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ComplaintListSerializer
        else:
            return ComplaintCreateSerializer


class ComplaintDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ComplaintDetailSerializer
    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        if self.request.user.my_houses.filter(
            kapt_name=self.kwargs["kapt_name"]
        ).exists():
            queryset = Complaint.objects.filter(
                house__kapt_name=self.kwargs["kapt_name"],
                pk=self.kwargs["pk"],
            ).select_related("user")
            return queryset
        raise PermissionDenied
