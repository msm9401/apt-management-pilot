from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import FeedListSerializer, FeedDetailSerializer
from comments.serializers import CommentDetailSerializer
from .models import Feed
from houses.models import Apartment


class FeedList(APIView):

    permission_classes = [IsAuthenticated]

    # 피드 리스트
    def get(self, request, kapt_name):
        if request.user.my_houses.filter(kapt_name=self.kwargs["kapt_name"]).exists():
            try:
                my_apt_pk = Apartment.objects.get(kapt_name=kapt_name).pk
                feed_list = Feed.objects.filter(house_id=my_apt_pk)
            except Apartment.DoesNotExist:
                raise NotFound
            serializer = FeedListSerializer(feed_list, many=True)
            return Response(serializer.data)
        raise PermissionDenied

    # 피드 생성
    def post(self, request, kapt_name):
        serializer = FeedDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                house=Apartment.objects.get(kapt_name=kapt_name),
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, kapt_name, pk):
        if self.request.user.my_houses.filter(
            kapt_name=self.kwargs["kapt_name"]
        ).exists():
            try:
                return Feed.objects.get(pk=pk)
            except Feed.DoesNotExist:
                raise NotFound
        raise PermissionDenied

    # 특정 피드 조회
    def get(self, request, kapt_name, pk):
        feed = self.get_object(kapt_name, pk)
        if feed.house.kapt_name != kapt_name:
            raise ParseError("존재하지 않는 피드입니다.")
        serializer = FeedDetailSerializer(feed)
        return Response(serializer.data)

    # 피드 수정
    def put(self, request, kapt_name, pk):
        feed = self.get_object(kapt_name, pk)
        if feed.user != request.user:
            raise PermissionDenied
        serializer = FeedDetailSerializer(feed, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
