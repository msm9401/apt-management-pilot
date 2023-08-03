from rest_framework import generics

from .serializers import NoticeDetailSerializer, NoticeListSerializer
from .models import Notice
from houses.models import Apartment
from common.permissions import IsAdminUserOrAuthenticatedReadOnly


class NoticeListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        queryset = Notice.objects.filter(house__kapt_code=kapt_code)
        return queryset

    def perform_create(self, serializer):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        serializer.save(house=Apartment.objects.get(kapt_code=kapt_code))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return NoticeListSerializer
        else:
            return NoticeDetailSerializer


class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoticeDetailSerializer
    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        queryset = Notice.objects.filter(
            house__kapt_code=kapt_code,
            pk=self.kwargs["pk"],
        )
        return queryset
