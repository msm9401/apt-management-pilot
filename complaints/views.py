from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

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
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        queryset = Complaint.objects.filter(house__kapt_code=kapt_code)
        return queryset

    def perform_create(self, serializer):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        serializer.save(
            house=Apartment.objects.get(kapt_code=kapt_code), user=self.request.user
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
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        queryset = Complaint.objects.filter(
            house__kapt_code=kapt_code,
            pk=self.kwargs["pk"],
        )
        return queryset
