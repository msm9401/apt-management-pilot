from django.urls import path

from . import views


urlpatterns = [
    path("", views.NoticeListCreate.as_view()),
    path("<int:pk>", views.NoticeDetail.as_view()),
]
