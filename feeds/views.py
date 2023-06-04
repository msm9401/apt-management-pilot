from django.shortcuts import get_list_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import status

from .serializers import FeedListSerializer, FeedDetailSerializer
from comments.serializers import CommentDetailSerializer
from .models import Feed
from houses.models import Apartment


class FeedList(APIView):
    permission_classes = [IsAuthenticated]

    # 피드 리스트
    def get(self, request, kapt_name):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = request.user.check_my_house(kapt_name=kapt_name)
        feed_list = get_list_or_404(
            Feed.objects.select_related("user").prefetch_related("comments", "photos"),
            house__kapt_code=kapt_code,
        )
        serializer = FeedListSerializer(feed_list, many=True)
        return Response(serializer.data)

    # 피드 생성
    def post(self, request, kapt_name):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = request.user.check_my_house(kapt_name=kapt_name)
        serializer = FeedDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            house=Apartment.objects.get(kapt_code=kapt_code),
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FeedDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, kapt_name, pk):
        kapt_name = self.kwargs["kapt_name"]
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        feed = get_object_or_404(
            Feed.objects.select_related("user"), house__kapt_code=kapt_code, pk=pk
        )
        return feed

    # 특정 피드 조회
    def get(self, request, kapt_name, pk):
        feed = self.get_object(kapt_name, pk)
        serializer = FeedDetailSerializer(feed)
        return Response(serializer.data)

    # 피드 수정
    def put(self, request, kapt_name, pk):
        feed = self.get_object(kapt_name, pk)
        if feed.user != request.user:
            raise PermissionDenied
        serializer = FeedDetailSerializer(feed, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # 피드에 대한 댓글 추가
    def post(self, request, kapt_name, pk):
        serializer = CommentDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                feed=self.get_object(kapt_name, pk),
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 피드 삭제
    def delete(self, request, kapt_name, pk):
        feed = self.get_object(kapt_name, pk)
        if feed.user != request.user:
            raise PermissionDenied
        feed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
