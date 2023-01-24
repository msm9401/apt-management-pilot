from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializers import FeedListSerializer, FeedDetailSerializer
from .models import Feed
from houses.models import Apartment


class FeedList(APIView):

    """
    내 아파트 피드 리스트
    """

    def get(self, request, kapt_name):
        my_apt_pk = Apartment.objects.get(kapt_name=kapt_name).pk
        feed_list = Feed.objects.filter(house_id=my_apt_pk)
        serializer = FeedListSerializer(feed_list, many=True)
        return Response(serializer.data)


class FeedDetail(APIView):
    def get_object(self, kapt_name, pk):
        try:
            return Feed.objects.get(pk=pk)
        except Feed.DoesNotExist:
            raise NotFound

    def get(self, request, kapt_name, pk):
        feed = self.get_object(kapt_name, pk)
        serializer = FeedDetailSerializer(feed)
        return Response(serializer.data)
