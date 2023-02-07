from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework import exceptions

from .models import User
from houses.serializers import ApartmentSerializer


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "profile_photo",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "profile_photo",
            "email",
            "phone_number",
        ]


class PublicUserProfileSerializer(serializers.ModelSerializer):

    feeds = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username",
            "profile_photo",
            "date_joined",
            "feeds",
            "comments",
        ]

    def get_feeds(self, user):
        feeds = self.context["feeds"]
        return feeds.data

    def get_comments(self, user):
        comments = self.context["comments"]
        return comments.data


class MyProfileSerializer(serializers.ModelSerializer):

    feeds = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    my_houses = ApartmentSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "username",
            "profile_photo",
            "name",
            "email",
            "my_houses",
            "phone_number",
            "apt_number",
            "house_number",
            "date_joined",
            "last_login",
            "feeds",
            "comments",
        ]

    def get_feeds(self, user):
        feeds = self.context["feeds"]
        return feeds.data

    def get_comments(self, user):
        comments = self.context["comments"]
        return comments.data


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        try:
            user = User(username=validated_data["username"])
            validate_password(validated_data["password"])
        except Exception as e:
            raise exceptions.ParseError(e)
        user.set_password(validated_data["password"])
        user.save()
        return user
