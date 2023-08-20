import random

from django.db.models import Max, Min
from django.db.models import Q
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

from .serializers import ApartmentSerializer
from .models import Apartment


class ApartmentList(APIView):

    """
    랜덤 아파트 리스트(로그인 안했을때)
    본인 아파트(로그인 했을때)
    """

    def get(self, request):
        # 로그인 했을때
        if not request.user.is_anonymous:
            cached_house = cache.get(f"{request.user}:house_list")
            if cached_house:
                return Response(cached_house)

            my_houses = request.user.my_houses
            serializer = ApartmentSerializer(my_houses, many=True)

            cache.set(f"{request.user}:house_list", serializer.data, 60)

            return Response(serializer.data)

        # 로그인 안했을때
        cached_random_house = cache.get("random_house_list")
        if cached_random_house:
            return Response(cached_random_house)

        max_apt_id = Apartment.objects.aggregate(max_apt_id=Max("id"))["max_apt_id"]
        min_apt_id = Apartment.objects.aggregate(min_apt_id=Min("id"))["min_apt_id"]

        if not max_apt_id:
            raise ParseError("아파트 정보를 불러올 수 없습니다.")

        random_apt_pk_list = []
        for _ in range(10):
            pk = random.randint(min_apt_id, max_apt_id)
            random_apt_pk_list.append(pk)

        random_apt_list = Apartment.objects.filter(id__in=random_apt_pk_list)
        serializer = ApartmentSerializer(random_apt_list, many=True)

        cache.set("random_house_list", serializer.data, 60 * 60)

        return Response(serializer.data)


class ApartmentDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, kapt_name, pk):
        apartment = get_object_or_404(Apartment, kapt_name=kapt_name, pk=pk)
        return apartment

    def get(self, request, kapt_name, pk):
        apartment = self.get_object(kapt_name, pk)
        serializer = ApartmentSerializer(apartment)
        return Response(serializer.data)

    # 임시
    # TODO : 실제 아파트 주민인지 검증하는 로직 필요
    def post(self, request, kapt_name, pk):
        apartment = self.get_object(kapt_name, pk)
        request.user.my_houses.add(apartment)
        return Response({"messages": "아파트 정보를 추가했습니다."})


class SearchApartment(APIView):

    """아파트 검색"""

    def get(self, request):
        if not request.query_params.get("keyword"):
            raise ParseError("검색어를 입력하세요.")
        if len(request.query_params.get("keyword")) == 1:
            raise ParseError("1글자 이상으로 검색하세요.")
        apt_searched = Apartment.objects.filter(
            Q(kapt_name__icontains=request.query_params.get("keyword"))
            | Q(address_do__icontains=request.query_params.get("keyword"))
            | Q(address_si__icontains=request.query_params.get("keyword"))
            | Q(address_dong__icontains=request.query_params.get("keyword"))
        )
        if not apt_searched:
            raise ParseError("찾으시는 결과가 없습니다.")
        serializers = ApartmentSerializer(apt_searched, many=True)
        return Response(serializers.data)
