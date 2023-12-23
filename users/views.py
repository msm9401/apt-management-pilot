from datetime import timedelta

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import get_object_or_404
from rest_framework import status
from guest_user.decorators import allow_guest_user

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from .models import User
from .serializers import (
    PublicUserProfileSerializer,
    MyProfileSerializer,
    UserUpdateSerializer,
    CreateUserSerializer,
    TinyUserSerializer,
)
from feeds.models import Feed
from comments.models import Comment
from feeds.serializers import FeedListSerializer
from comments.serializers import CommentDetailSerializer
from houses.models import Apartment


class PublicUserProfile(APIView):

    """공개 프로필"""

    permission_classes = [IsAuthenticated]

    def get(self, request, kapt_name, username):
        user = get_object_or_404(User, username=username)
        feeds = Feed.objects.filter(user=user, house__kapt_name=kapt_name)
        comments = Comment.objects.filter(
            user=user,
            feed__house__kapt_name=kapt_name,
        )
        serializer = PublicUserProfileSerializer(
            user,
            context={
                "feeds": FeedListSerializer(feeds, many=True),
                "comments": CommentDetailSerializer(comments, many=True),
            },
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyProfile(APIView):

    """내 프로필"""

    permission_classes = [IsAuthenticated]

    def get(self, request, kapt_name):
        user = request.user
        feeds = (
            Feed.objects.select_related("user")
            .prefetch_related("comments", "photos")
            .filter(user=user, house__kapt_name=kapt_name)
        )
        comments = Comment.objects.select_related("user").filter(
            user=user,
            feed__house__kapt_name=kapt_name,
        )
        serializer = MyProfileSerializer(
            user,
            context={
                "feeds": FeedListSerializer(feeds, many=True),
                "comments": CommentDetailSerializer(comments, many=True),
            },
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, kapt_name):
        user = request.user
        serializer = UserUpdateSerializer(
            user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)  # 400
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateAccount(APIView):

    """회원 가입"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 400
        user = serializer.save()
        serializer = CreateUserSerializer(user)
        return Response(
            {
                "user": serializer.data,
                "token": AuthToken.objects.create(user)[1],
            },
            status=status.HTTP_201_CREATED,
        )


class LogIn(KnoxLoginView):

    """로그인"""

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 400
        user = serializer.validated_data["user"]
        serializer = TinyUserSerializer(user)
        return Response(
            {
                "user": serializer.data,
                "token": AuthToken.objects.create(user)[1],
            },
            status=status.HTTP_200_OK,
        )


@allow_guest_user
def hello_guest(request):
    """
    - 게스트 유저 로그인에 필요한 토큰과 아파트 미리 설정
    - 토큰 반환함으로 프론트에서 받아서 바로 로그인 시키면 됨.
    - {"token": str}
    """
    # 게스트 유저에 필요한 토큰 생성
    temp_token = AuthToken.objects.create(
        user=request.user,
        expiry=timedelta(days=1),
    )[1]

    # 게스트 유저의 아파트 설정 후 저장
    temp_house = Apartment.objects.filter(kapt_name__in=["용인신갈푸르지오", "분당 파크뷰"])
    list(map(lambda house: request.user.my_houses.add(house), temp_house))

    request.user.save()

    return JsonResponse({"token": temp_token})
