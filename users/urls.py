from django.urls import path

from knox import views as knox_views

from . import views

urlpatterns = [
    path("signup", views.CreateAccount.as_view()),
    path("login", views.LogIn.as_view()),
    path("logout", knox_views.LogoutView.as_view()),
    path("logoutall", knox_views.LogoutAllView.as_view()),
    path("myprofile", views.MyProfile.as_view()),
    path("@<str:username>", views.PublicUserProfile.as_view()),
]
