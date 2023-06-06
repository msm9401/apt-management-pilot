from django.urls import reverse

from rest_framework.test import APITestCase

from users.models import User
from houses.models import Apartment
from .models import Notice


class NoticeListTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        "공지사항 테스트"에 필요한 유저, 아파트, 공지사항 미리 세팅
        """

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
        """공지사항 불러오기 테스트"""

        # 유저 아파트 설정 전 접근
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 403)

        # 유저 아파트 설정
        self.user.my_houses.add(self.apt)
        self.user.save()

        # 본인 아파트의 공지사항에 성공적으로 접근
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]["title"], self.notice_data["title"])

    def test_create_notice(self):
        """공지사항 생성 테스트"""

        # 유저 아파트 설정 전 접근
        response = self.client.post(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 403)

        # 유저 아파트 설정
        # 관리자만 공지사항 추가 가능.
        self.user.my_houses.add(self.apt)
        # self.user.is_admin = True
        self.user.is_staff = True
        self.user.save()

        # 본인 아파트에 성공적으로 공지사항 생성
        response = self.client.post(
            path=self.url,
            data=self.notice_data,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 201)
