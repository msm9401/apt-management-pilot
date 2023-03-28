from django.urls import reverse

from rest_framework.test import APITestCase

from users.models import User
from houses.models import Apartment
from .models import ContactNumber


class ContactListTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        """
        "연락처 테스트"에 필요한 유저, 아파트, 연락처 미리 세팅
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
        cls.contact_data = {
            "contact_to": "관리사무소",
            "contact_number": "1234",
        }
        cls.contact = ContactNumber.objects.create(
            contact_to="관리사무소", contact_number="1234", house=cls.apt
        )
        cls.url = "/api/v1/houses/푸르지오/contact/"

    def setUp(self):
        data = self.client.post(reverse("login"), self.user_data).data
        self.token = data["token"]

    def test_get_contact_list(self):

        """
        본인 아파트 연락처에만 접근 가능하지 테스트
        본인 아파트가 아닐때 의도적으로 403오류 나오는지 테스트 그리고
        본인 아파트 정보를 입력하고 접근가능한지 테스트
        """

        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        print("'Forbidden' is the intended message.")
        self.assertEqual(response.status_code, 403)  # 유저의 집이 저장 안되어있을때(본인 아파트가 아닐때)

        self.user.my_houses.add(self.apt)  # 유저의 집 저장
        self.user.save()
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 200)  # 유저의 집 저장 되어있을때
        self.assertIsInstance(response.data, list)
        self.assertEqual(
            response.data[0]["contact_to"], self.contact_data["contact_to"]
        )

    def test_create_contact(self):
        response = self.client.post(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        print("'Forbidden' is the intended message.")
        self.assertEqual(response.status_code, 403)

        self.user.my_houses.add(self.apt)
        # self.user.is_admin = True
        self.user.is_staff = True  # 관리자만 연락처 추가 가능.
        self.user.save()
        response = self.client.post(
            path=self.url,
            data=self.contact_data,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 201)
