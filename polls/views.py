from datetime import datetime

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import F
from django.core.cache import cache
from django.utils import timezone

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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
        queryset = Question.objects.filter(house__kapt_code=kapt_code, status=True)
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


# 선택지 상세정보
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAdminUserOrAuthenticatedReadOnly])
def choice_detail(request, kapt_name, pk, choice_pk):
    kapt_code = request.user.check_my_house(kapt_name=kapt_name)

    question = get_object_or_404(
        Question.objects.filter(house__kapt_code=kapt_code), pk=pk
    )
    selected_choice = get_object_or_404(Choice, question=question, pk=choice_pk)

    if request.method == "GET":
        serializer = ChoiceDetailSerializer(selected_choice)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


# 선택지 투표
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def vote(request, kapt_name, pk, choice_pk):
    kapt_code = request.user.check_my_house(kapt_name=kapt_name)

    question = get_object_or_404(
        Question.objects.filter(house__kapt_code=kapt_code), pk=pk
    )
    selected_choice = get_object_or_404(Choice, question=question, pk=choice_pk)

    if request.method == "GET":
        serializer = ChoiceDetailSerializer(selected_choice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        # 투표 했는지 확인
        voted_check = cache.get(
            f"{question.title.replace(' ','')}:voted_user:{request.user}"
        )

        # 캐시 hit시 투표 block
        if voted_check:
            return Response(
                {
                    "detail": "이미 투표를 마쳤습니다.",
                    "status_code": status.HTTP_403_FORBIDDEN,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # 투표가 닫혔을때 block
        if question.status == False:
            return Response(
                {
                    "detail": "투표가 닫혔습니다.",
                    "status_code": status.HTTP_403_FORBIDDEN,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # 투표 시간 설정을 했을 때 ttl
        # 투표 시간이 지났다면 투표 block
        # 추가로 604800(7일) 더해준 이유는 투표율 저조로 인해서 투표기간이 늘어날 경우를 대비
        if question.end_date is not None:
            time = question.end_date - datetime.now(tz=timezone.utc)

            if time.days > 0:
                ttl = (time.days * 24 * 60 * 60) + time.seconds + 604800
            elif time.days < 0:
                return Response(
                    {
                        "detail": "투표 시간이 지났습니다.",
                        "status_code": status.HTTP_403_FORBIDDEN,
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            else:
                ttl = time.seconds + 604800

        # 투표 시간 설정을 안했을 때 ttl 14일로 설정
        else:
            ttl = 1209600  # 14일

        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # ttl 30초 시간 설정은 임시(배포 시 ttl값으로 변경 예정)
        # 캐시 key에 공백 있을시 에러발생
        cache.set(f"{question.title.replace(' ','')}:voted_user:{request.user}", 1, ttl)

        return Response(status=status.HTTP_200_OK)
