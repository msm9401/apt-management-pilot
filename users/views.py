from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import get_object_or_404
from rest_framework import status

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
