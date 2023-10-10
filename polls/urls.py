from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("", views.QuestionListCreate.as_view(), name="question"),
    path("<int:pk>", views.QuestionDetail.as_view(), name="question-detail"),
    path("<int:pk>/choice", views.ChoiceListCreate.as_view(), name="choice"),
    path("<int:pk>/choice/<int:choice_pk>", views.vote, name="vote"),
]
