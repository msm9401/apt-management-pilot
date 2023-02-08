from django.shortcuts import get_list_or_404

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied

from common.permissions import IsAdminUserOrAuthenticatedReadOnly
from houses.models import Apartment
from .models import Question
from .serializers import QuestionListSerializer, QuestionDetailSerializer


class QuestionListCreate(generics.ListCreateAPIView):

    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        if self.request.user.my_houses.filter(
            kapt_name=self.kwargs["kapt_name"]
        ).exists():
            queryset = Question.objects.filter(
                house__kapt_name=self.kwargs["kapt_name"]
            )
            return get_list_or_404(queryset)
        raise PermissionDenied

    def perform_create(self, serializer):
        serializer.save(house=Apartment.objects.get(kapt_name=self.kwargs["kapt_name"]))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return QuestionListSerializer
        else:
            return QuestionDetailSerializer


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = QuestionDetailSerializer
    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        if self.request.user.my_houses.filter(
            kapt_name=self.kwargs["kapt_name"]
        ).exists():
            queryset = Question.objects.filter(
                house__kapt_name=self.kwargs["kapt_name"],
                pk=self.kwargs["pk"],
            )
            return queryset
        raise PermissionDenied
