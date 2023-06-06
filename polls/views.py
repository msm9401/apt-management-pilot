from rest_framework import generics

from common.permissions import IsAdminUserOrAuthenticatedReadOnly
from houses.models import Apartment
from .models import Question
from .serializers import QuestionListSerializer, QuestionDetailSerializer


class QuestionListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        queryset = Question.objects.filter(house__kapt_code=kapt_code)
        return queryset

    def perform_create(self, serializer):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        serializer.save(house=Apartment.objects.get(kapt_code=kapt_code))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return QuestionListSerializer
        else:
            return QuestionDetailSerializer


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionDetailSerializer
    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        queryset = Question.objects.filter(
            house__kapt_code=kapt_code,
            pk=self.kwargs["pk"],
        )
        return queryset


# TODO : Choice기능 만들어야 함
