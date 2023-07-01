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
        """피드 불러오기 테스트"""

        # 유저 아파트 설정 전 접근
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 403)

        # 유저 아파트 설정
        self.user.my_houses.add(self.apt)
        self.user.save()

        # 본인 아파트의 feed에 성공적으로 접근
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]["content"], self.feed.content)
        self.assertEqual(response.data[0]["user"]["username"], self.feed.user.username)

    def test_create_feed(self):
        """피드 생성 테스트"""

        # 유저 아파트 설정 전 접근
        response = self.client.post(
            self.url,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 403)

        # 유저 아파트 설정
        self.user.my_houses.add(self.apt)
        self.user.save()

        # 본인 아파트에 성공적으로 feed생성
        response = self.client.post(
            path=self.url,
            data=self.feed_data,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 201)

        # 필수값인 content에 data없이 post
        response = self.client.post(
            path=self.url,
            data={"content": ""},
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 400)

    def test_get_feed_datial(self):
        """특정 피드 접근 테스트"""

        # 유저 아파트 설정 전 접근
        response = self.client.get(
            path=self.url + "1/",
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 403)

        # 유저 아파트 설정
        self.user.my_houses.add(self.apt)
        self.user.save()

        # 본인 아파트에 성공적으로 feed생성
        response = self.client.post(
            path=self.url,
            data=self.feed_data,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 201)

        # 본인 아파트의 특정feed에 성공적으로 접근
        pk = response.data["id"]
        response = self.client.get(
            path=self.url + str(pk) + "/",
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 200)

        # 본인 아파트의 존재하지 않은 feed에 접근
        response = self.client.get(
            path=self.url + str(pk + 1) + "/",
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 404)

    def test_put_feed(self):
        """피드 수정 테스트"""

        # 유저 아파트 설정(저장)
        self.user.my_houses.add(self.apt)
        self.user.save()

        # 본인 아파트에 성공적으로 feed생성
        response = self.client.post(
            path=self.url,
            data=self.feed_data,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 201)

        # 아무 정보 없이 수정
        pk = response.data["id"]
        response = self.client.put(
            path=self.url + str(pk) + "/",
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 200)

        # 피드 내용 수정
        response = self.client.put(
            path=self.url + str(pk) + "/",
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

        # 본인 아파트에 성공적으로 feed생성
        response = self.client.post(
            path=self.url,
            data=self.feed_data,
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 201)

        # 피드 삭제
        pk = response.data["id"]
        response = self.client.delete(
            path=self.url + str(pk) + "/",
            HTTP_AUTHORIZATION=f"token {self.token}",
        )
        self.assertEqual(response.status_code, 204)
