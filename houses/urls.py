from django.urls import path

from . import views


urlpatterns = [
    path("", views.ApartmentList.as_view()),
    path("search", views.SearchApartment.as_view()),
]
