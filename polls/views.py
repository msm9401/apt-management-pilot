from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import F

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from common.permissions import IsAdminUserOrAuthenticatedReadOnly
from houses.models import Apartment
from .models import Question, Choice
from .serializers import (
    QuestionListSerializer,
    QuestionDetailSerializer,
    ChoiceListSerializer,
    ChoiceDetailSerializer,
)


# 투표 리스트 및 생성
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


# 투표 상세정보
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionDetailSerializer
    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        queryset = Question.objects.filter(
            house__kapt_code=kapt_code,
            pk=self.kwargs["pk"],
        )
        return queryset


# 투표의 선택지 리스트 및 선택지 생성
class ChoiceListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUserOrAuthenticatedReadOnly]

    def get_queryset(self):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        question = get_object_or_404(
            Question.objects.filter(house__kapt_code=kapt_code), pk=self.kwargs["pk"]
        )
        queryset = Choice.objects.filter(question=question)
        return queryset

    def perform_create(self, serializer):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        question = get_object_or_404(
            Question.objects.filter(house__kapt_code=kapt_code), pk=self.kwargs["pk"]
        )
        serializer.save(question=question)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChoiceListSerializer
        else:
            return ChoiceDetailSerializer


# 선택지 투표 및 조작
@api_view(["GET", "POST", "PUT", "DELETE"])
def vote(request, kapt_name, pk, choice_pk):
    kapt_code = request.user.check_my_house(kapt_name=kapt_name)

    question = get_object_or_404(
        Question.objects.filter(house__kapt_code=kapt_code), pk=pk
    )
    selected_choice = get_object_or_404(Choice, question=question, pk=choice_pk)

    if request.method == "GET":
        serializer = ChoiceDetailSerializer(selected_choice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 투표
    elif request.method == "POST":
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # 투표 목록으로 redirect
        return HttpResponseRedirect(
            reverse("polls:question", kwargs={"kapt_name": kapt_name}),
            status=status.HTTP_302_FOUND,
        )  # 302

    # 선택지 수정
    elif request.method == "PUT":
        serializer = ChoiceDetailSerializer(
            selected_choice, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 선택지 삭제
    elif request.method == "DELETE":
        selected_choice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
