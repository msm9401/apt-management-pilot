from django.urls import reverse

from rest_framework.test import APITestCase

from .models import User


class UserRegistrationTest(APITestCase):
    def test_signup(self):
        url = reverse("signup")
        data = {
            "username": "testuser",
            "password": "password@123",
        }
        response = self.client.post(url, data)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["user"]["username"], "testuser")


class UserTest(APITestCase):
    def setUp(self):
        self.data = {
            "username": "testuser",
            "password": "password@123",
        }
        self.user = User.objects.create_user(
            username="testuser",
            password="password@123",
        )

    # 로그인
    def test_login(self):
        url = reverse("login")
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, 200)

    # 내 프로필
    def test_get_myprofile(self):
        url = "/api/v1/users/<str:kapt_name>/profile/myprofile"
        token = self.client.post(reverse("login"), self.data).data["token"]
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f"token {token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.data["username"])

    # 내 프로필 수정
    def test_modify_myprofile(self):
        url = "/api/v1/users/<str:kapt_name>/profile/myprofile"
        token = self.client.post(reverse("login"), self.data).data["token"]
        response = self.client.put(
            url,
            HTTP_AUTHORIZATION=f"token {token}",
            data={"phone_number": "01033334444"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["phone_number"], "01033334444")

    # 유저 프로필
    def test_get_user_profile(self):
        login_user = self.client.post(reverse("login"), self.data)
        username = login_user.data["user"]["username"]
        token = login_user.data["token"]
        response = self.client.get(
            path=f"/api/v1/users/<str:kapt_name>/profile/@{username}",
            HTTP_AUTHORIZATION=f"token {token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.data["username"])

    # 로그 아웃
    def test_logout(self):
        url = reverse("logout")
        token = self.client.post(reverse("login"), self.data).data["token"]
        response = self.client.post(
            url,
            HTTP_AUTHORIZATION=f"token {token}",
        )

        self.assertEqual(response.status_code, 204)
