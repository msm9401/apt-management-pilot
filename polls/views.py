from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from common.permissions import IsAdminUserOrAuthenticatedReadOnly
from houses.models import Apartment
from .models import Question
from .serializers import QuestionListSerializer, QuestionDetailSerializer


class QuestionListCreate(generics.ListCreateAPIView):

    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        my_apt = self.request.user.my_houses.filter(kapt_name=self.kwargs["kapt_name"])
        if my_apt:
            queryset = Question.objects.filter(house=my_apt[0])
            return queryset
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
