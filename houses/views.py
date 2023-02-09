import random

from django.db.models import Max, Min
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from .serializers import ApartmentSerializer
from .models import Apartment


class ApartmentList(APIView):

    """
    랜덤 아파트 리스트(로그인 안했을때)
    본인 아파트(로그인 했을때)
    """

    def get(self, request):
        if not request.user.is_anonymous:
            my_houses = request.user.my_houses
            serializer = ApartmentSerializer(my_houses, many=True)
            return Response(serializer.data)
        max_apt_id = Apartment.objects.aggregate(max_apt_id=Max("id"))["max_apt_id"]
        min_apt_id = Apartment.objects.aggregate(min_apt_id=Min("id"))["min_apt_id"]
        random_apt_list = []
        for i in range(1, 11):
            pk = random.randint(min_apt_id, max_apt_id)
            try:
                random_apt = Apartment.objects.get(pk=pk)
                random_apt_list.append(random_apt)
            except Apartment.DoesNotExist:
                pass
        serializer = ApartmentSerializer(random_apt_list, many=True)
        return Response(serializer.data)


class SearchApartment(APIView):

    """
    특정 아파트 검색(아파트 이름으로 검색 추천)
    """

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
