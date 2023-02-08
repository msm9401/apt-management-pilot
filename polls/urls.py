from django.urls import path

from . import views


urlpatterns = [
    path("", views.QuestionListCreate.as_view()),
    path("<int:pk>", views.QuestionDetail.as_view()),
]
