from django.shortcuts import get_list_or_404

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied

from .serializers import ScheduleSerializer
from .models import Schedule
from houses.models import Apartment
from common.permissions import IsAdminUserOrAuthenticatedReadOnly


class ScheduleListCreate(generics.ListCreateAPIView):

    serializer_class = ScheduleSerializer
    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        if self.request.user.my_houses.filter(
            kapt_name=self.kwargs["kapt_name"]
        ).exists():  # 유저 본인의 집(아파트)인지 확인
            queryset = Schedule.objects.filter(
                house__kapt_name=self.kwargs["kapt_name"]
            )
            return get_list_or_404(queryset)
        raise PermissionDenied

    def perform_create(self, serializer):
        serializer.save(house=Apartment.objects.get(kapt_name=self.kwargs["kapt_name"]))


class ScheduleDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ScheduleSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.my_houses.filter(
            kapt_name=self.kwargs["kapt_name"]
        ).exists():
            queryset = Schedule.objects.filter(
                house__kapt_name=self.kwargs["kapt_name"],
                pk=self.kwargs["pk"],
            )
            return queryset
        raise PermissionDenied
