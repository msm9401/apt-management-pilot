from django.urls import path

from . import views


urlpatterns = [
    path("", views.ContactListCreate.as_view()),
    path("<int:pk>", views.ContactDetail.as_view()),
]
