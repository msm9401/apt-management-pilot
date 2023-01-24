from django.urls import path

from . import views


urlpatterns = [
    path("", views.FeedList.as_view()),
    path("<int:pk>", views.FeedDetail.as_view()),
]
