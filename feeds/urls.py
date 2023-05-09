from django.urls import path, include

from . import views


urlpatterns = [
    path("", views.FeedList.as_view(), name="feed"),
    path("<int:pk>/", views.FeedDetail.as_view()),
    path("<int:pk>/comment/", include("comments.urls")),
]
