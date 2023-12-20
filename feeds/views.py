from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from guest_user.functions import is_guest_user

from .serializers import FeedListSerializer, FeedDetailSerializer
from comments.serializers import CommentDetailSerializer
from .models import Feed
from houses.models import Apartment
from medias.models import Photo
from config.pagination import PaginationHandlerMixin
from .tasks import upload_photo


class FeedPagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_size = 5


class FeedList(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]
    pagination_class = FeedPagination

    # 피드 리스트
    def get(self, request, kapt_name):
        kapt_code = request.user.check_my_house(kapt_name=kapt_name)

        feed_list = (
            Feed.objects.select_related("user")
            .prefetch_related("comments", "photos")
            .filter(house__kapt_code=kapt_code)
        )

        page = self.paginate_queryset(feed_list)

        if page is None:
            serializer = FeedListSerializer(feed_list, many=True)
        serializer = self.get_paginated_response(
            FeedListSerializer(page, many=True).data
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    # 피드 생성
    def post(self, request, kapt_name):
        # 게스트 유저는 피드 생성 금지
        if is_guest_user(request.user):
            raise PermissionDenied

        kapt_code = request.user.check_my_house(kapt_name=kapt_name)

        serializer = FeedDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 400
        new_feed = serializer.save(
            user=request.user,
            house=Apartment.objects.get(kapt_code=kapt_code),
        )

        if request.FILES:
            new_photo = Photo(
                user=request.user,
                house=Apartment.objects.get(kapt_code=kapt_code),
                file=request.FILES["photos[]"],
                feed=new_feed,
            )
            new_photo.save()
            upload_photo.delay(new_photo.file.name)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FeedDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, kapt_name, pk):
        kapt_code = self.request.user.check_my_house(kapt_name=kapt_name)
        feed = get_object_or_404(
            Feed.objects.select_related("user"), house__kapt_code=kapt_code, pk=pk
        )
        return feed

    # 특정 피드 조회
    def get(self, request, kapt_name, pk):
        feed = self.get_object(kapt_name, pk)
        serializer = FeedDetailSerializer(feed)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 피드 수정
    def put(self, request, kapt_name, pk):
        feed = self.get_object(kapt_name, pk)
        if feed.user != request.user:
            raise PermissionDenied  # 403
        serializer = FeedDetailSerializer(feed, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)  # 400
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 피드에 대한 댓글 추가
    def post(self, request, kapt_name, pk):
        # 게스트 유저는 댓글 생성 금지
        if is_guest_user(request.user):
            raise PermissionDenied

        serializer = CommentDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 400
        serializer.save(
            user=request.user,
            feed=self.get_object(kapt_name, pk),
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 피드 삭제
    def delete(self, request, kapt_name, pk):
        feed = self.get_object(kapt_name, pk)
        if feed.user != request.user:
            raise PermissionDenied  # 403
        feed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
