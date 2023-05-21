from django.urls import path

from knox import views as knox_views

from . import views


urlpatterns = [
    path("signup", views.CreateAccount.as_view(), name="signup"),
    path("login", views.LogIn.as_view(), name="login"),
    path("logout", knox_views.LogoutView.as_view(), name="logout"),
    # path("logout", views.LogOut.as_view(), name="logout"),
    path("logoutall", knox_views.LogoutAllView.as_view(), name="logout_all"),
    # path("myprofile", views.MyProfile.as_view(), name="my_profile"),
    # path("@<str:username>", views.PublicUserProfile.as_view(), name="public_profile"),
    path(
        "<str:kapt_name>/profile/myprofile",
        views.MyProfile.as_view(),
        name="my_profile",
    ),
    path(
        "<str:kapt_name>/profile/@<str:username>",
        views.PublicUserProfile.as_view(),
        name="public_profile",
    ),
]
