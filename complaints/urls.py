from django.urls import path

from . import views

urlpatterns = [
    path("", views.ComplaintListCreate.as_view()),
    path("<int:pk>", views.ComplaintDetail.as_view()),
]
