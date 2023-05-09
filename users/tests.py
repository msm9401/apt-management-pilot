from django.urls import reverse

from rest_framework.test import APITestCase

from .models import User


class UserRegistrationTest(APITestCase):
    def test_signup(self):
        url = reverse("signup")
        # url = "/api/v1/users/signup"
        data = {
            "username": "testuser",
            "password": "password@123",
        }
        response = self.client.post(url, data)
        result = response.json()

        self.assertEqual(response.status_code, 200)
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
        # url = "/api/v1/users/login"
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, 200)

    # 내 프로필
    def test_get_myprofile(self):
        # url = reverse("my_profile")
        url = "/api/v1/users/<str:kapt_name>/profile/myprofile"
        token = self.client.post("/api/v1/users/login", self.data).data["token"]
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f"token {token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.data["username"])

    # 내 프로필 수정
    def test_modify_myprofile(self):
        # url = reverse("my_profile", kapt_name=self. 피드테스트처럼 미리 데이터 세팅하는게 편할듯?)
        url = "/api/v1/users/<str:kapt_name>/profile/myprofile"
        token = self.client.post("/api/v1/users/login", self.data).data["token"]
        response = self.client.put(
            url,
            HTTP_AUTHORIZATION=f"token {token}",
            data={"phone_number": "01033334444"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["phone_number"], "01033334444")

    # 유저 프로필
    def test_get_user_profile(self):
        user = self.client.post("/api/v1/users/login", self.data).data["user"][
            "username"
        ]
        response = self.client.get(f"/api/v1/users/<str:kapt_name>/profile/@{user}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.data["username"])

    # 로그 아웃
    def test_logout(self):
        url = "/api/v1/users/logout"
        token = self.client.post("/api/v1/users/login", self.data).data["token"]
        response = self.client.post(
            url,
            HTTP_AUTHORIZATION=f"token {token}",
        )

        self.assertEqual(response.status_code, 204)
