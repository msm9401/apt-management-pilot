from django.contrib.auth import login
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
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
        try:
            user = User.objects.get(username=username)
            feeds = Feed.objects.filter(user=user, house__kapt_name=kapt_name)
            comments = Comment.objects.filter(
                user=user,
                feed__house__kapt_name=kapt_name,
            )
        except User.DoesNotExist:
            raise NotFound
        serializer = PublicUserProfileSerializer(
            user,
            context={
                "feeds": FeedListSerializer(feeds, many=True),
                "comments": CommentDetailSerializer(comments, many=True),
            },
        )
        return Response(serializer.data)


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
        return Response(serializer.data)

    def put(self, request, kapt_name):
        user = request.user
        serializer = UserUpdateSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CreateAccount(APIView):

    """회원 가입"""

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            serializer = CreateUserSerializer(user)
            return Response(
                {
                    "user": serializer.data,
                    "token": AuthToken.objects.create(user)[1],
                }
            )
        return Response(serializer.errors)


class LogIn(KnoxLoginView):

    """로그인"""

    permission_classes = [AllowAny]

    # 로그인 되어있으면 로그인url로 접속시 홈화면으로 연결
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        serializer = TinyUserSerializer(user)
        return Response(
            {
                "user": serializer.data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


# 인증부분은 프론트할때 마무리하자.(토큰발급후 토큰으로 myprofile 확인함.)
