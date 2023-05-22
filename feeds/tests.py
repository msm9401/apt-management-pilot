from django.urls import reverse

from rest_framework.test import APITestCase
from .models import Feed
from users.models import User
from houses.models import Apartment


class FeedTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        "피드 테스트"에 필요한 유저, 아파트, 피드 미리 세팅
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
        cls.feed_data = {
            "content": "Feed Test",
        }
        cls.url = "/api/v1/houses/푸르지오/feed/"

    def setUp(self):
        data = self.client.post(reverse("login"), self.user_data).data
        self.token = data["token"]
        self.feed = Feed.objects.create(
            content="Feed Test", house=self.apt, user=self.user
        )

    def test_get_feed_list(self):
        """
        유저의 아파트랑 url의 아파트이름이 같지않거나 유저가 아파트가 존재하지 않을때 접근금지 테스트
        유저의 아파트가 url의 아파트이름이 같으면 접근가능 테스트
        """

        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )  # 접근불가능한지 의도적으로 오류
        print("'Forbidden' is the intended message.")
        self.assertEqual(response.status_code, 403)  # 유저의 집이 저장 안되어있을때 403오류

        self.user.my_houses.add(self.apt)  # 유저의 집 저장
        self.user.save()
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 200)  # 유저의 집 저장 되어있을때
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]["content"], self.feed.content)
        self.assertEqual(response.data[0]["house"], self.feed.house.id)
        self.assertEqual(response.data[0]["user"]["username"], self.feed.user.username)

    def test_create_feed(self):
        response = self.client.post(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )  # 의도적인 오류
        print("'Bad Request' is the intended message.")
        self.assertEqual(response.status_code, 400)

        self.user.my_houses.add(self.apt)
        self.user.save()
        response = self.client.post(
            path=self.url,
            data=self.feed_data,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_get_feed_datial(self):
        """
        특정 피드 접근 테스트
        """

        response = self.client.get(
            path=self.url + "1/",
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 403)

        self.user.my_houses.add(self.apt)
        self.user.save()
        response = self.client.get(
            path=self.url + "1/",
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            path=self.url + "2/",
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 404)

    def test_put_feed(self):
        """피드 수정 테스트"""

        # 유저 아파트 설정(저장)
        self.user.my_houses.add(self.apt)
        self.user.save()

        # 아무 정보 없이 수정
        response = self.client.put(
            path=self.url + "1/",
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 200)

        # 피드 내용 수정
        response = self.client.put(
            path=self.url + "1/",
            HTTP_AUTHORIZATION=f"token {self.token}",
            data={
                "content": "test2",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["content"], "test2")

    def test_delete_feed(self):
        """피드 삭제 테스트"""

        # 유저 아파트 설정(저장)
        self.user.my_houses.add(self.apt)
        self.user.save()

        # 피드 삭제
        response = self.client.delete(
            path=self.url + "1/",
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 204)
