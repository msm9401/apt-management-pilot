from django.urls import path

from . import views


urlpatterns = [
    path("", views.ScheduleListCreate.as_view()),
    path("<int:pk>", views.ScheduleDetail.as_view()),
]
