from django.urls import reverse

from rest_framework.test import APITestCase

from users.models import User
from houses.models import Apartment
from .models import Notice


class NoticeListTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "username": "testuser",
            "password": "password@123",
        }
        cls.user = User.objects.create_user(
            username="testuser",
            password="password@123",
        )
        cls.apt_data = {
            "address_do": "경기도",
            "address_si": "성남시",
            "address_dong": "정자동",
            "address_li": "",
            "bjd_code": "123",
            "kapt_code": "345",
            "kapt_name": "푸르지오",
        }
        cls.apt = Apartment.objects.create(
            address_do="경기도",
            address_si="성남시",
            address_dong="정자동",
            address_li="",
            bjd_code="123",
            kapt_code="345",
            kapt_name="푸르지오",
        )
        cls.notice_data = {
            "title": "Notice Test",
            "content": "Notice Content Test",
        }
        cls.notice = Notice.objects.create(
            title="Notice Test", content="Notice Content Test", house=cls.apt
        )
        cls.url = "/api/v1/houses/푸르지오/notice/"

    def setUp(self):
        data = self.client.post(reverse("login"), self.user_data).data
        self.token = data["token"]

    def test_get_notice_list(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 403)  # 유저의 집이 저장 안되어있을때

        self.user.my_houses.add(self.apt)  # 유저의 집 저장
        self.user.save()
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 200)  # 유저의 집 저장 되어있을때
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]["title"], self.notice_data["title"])

    def test_create_notice(self):
        response = self.client.post(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 403)

        self.user.my_houses.add(self.apt)
        # self.user.is_admin = True
        self.user.is_staff = True  # 관리자만 공지사항 추가 가능.
        self.user.save()
        response = self.client.post(
            path=self.url,
            data=self.notice_data,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 201)
