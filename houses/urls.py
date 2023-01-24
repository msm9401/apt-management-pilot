from django.urls import path
from . import views


urlpatterns = [
    path("", views.ApartmentRandomList.as_view()),  # 홈화면
    path("", views.SearchApartment.as_view()),
    path("<str:kapt_name>", views.MyApartment.as_view()),
]
