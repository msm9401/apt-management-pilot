from django.shortcuts import get_list_or_404

from rest_framework import generics

from .serializers import NoticeDetailSerializer, NoticeListSerializer
from .models import Notice
from houses.models import Apartment
from common.permissions import IsAdminUserOrAuthenticatedReadOnly


class NoticeListCreate(generics.ListCreateAPIView):

    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        queryset = Notice.objects.filter(house__kapt_name=self.kwargs["kapt_name"])
        return get_list_or_404(queryset)

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
        queryset = Notice.objects.filter(
            house__kapt_name=self.kwargs["kapt_name"],
            pk=self.kwargs["pk"],
        )
        return queryset
