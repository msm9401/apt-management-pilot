from django.shortcuts import get_list_or_404

from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from .serializers import NoticeDetailSerializer, NoticeListSerializer
from .models import Notice
from houses.models import Apartment
from common.permissions import IsAdminUserOrAuthenticatedReadOnly


class NoticeListCreate(generics.ListCreateAPIView):

    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        my_apt = self.request.user.my_houses.filter(kapt_name=self.kwargs["kapt_name"])
        if my_apt:
            queryset = Notice.objects.filter(house=my_apt[0])
            return queryset
        raise PermissionDenied

    def perform_create(self, serializer):
        serializer.save(house=Apartment.objects.get(kapt_name=self.kwargs["kapt_name"]))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return NoticeListSerializer
        else:
            return NoticeDetailSerializer


class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = NoticeDetailSerializer
    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        if self.request.user.my_houses.filter(
            kapt_name=self.kwargs["kapt_name"]
        ).exists():
            queryset = Notice.objects.filter(
                house__kapt_name=self.kwargs["kapt_name"],
                pk=self.kwargs["pk"],
            )
            return queryset
        raise PermissionDenied

    # 투표 기능 프론트할때 하자.
