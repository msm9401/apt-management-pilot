import random

from django.db.models import Max, Min
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import ParseError, NotFound

# from rest_framework import generics
# from rest_framework import filters

from .serializers import ApartmentSerializer
from .models import Apartment


class ApartmentRandomList(APIView):

    """
    랜덤 아파트 리스트
    """

    def get(self, request):
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
    특정 아파트 검색(아파트 이름으로 검색)
    """

    def get(self, request):
        try:
            text = request.query_params.get("search", "")
            text = str(text)
        except:
            text = ""
        if text != "":
            apt_searched = Apartment.objects.filter(kapt_name__contains=text)
        else:
            raise ParseError("검색어를 입력하세요.")
        serializers = ApartmentSerializer(apt_searched, many=True)
        return Response(serializers.data)


""" class SearchApartment(generics.ListAPIView):

    queryset = Apartment.objects.all()
    serialzer_class = ApartmentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "address_do",
        "address_si",
        "address_dong",
        "address_li",
        "kapt_name",
    ] """


class MyApartment(APIView):

    """
    내 아파트
    """

    def get(self, request, kapt_name):
        try:
            my_apt = Apartment.objects.get(kapt_name=kapt_name)
        except Apartment.DoesNotExist:
            raise NotFound
        serializer = ApartmentSerializer(my_apt)
        return Response(serializer.data)
