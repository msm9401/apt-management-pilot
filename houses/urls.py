from django.urls import path, include

# from users import views as users_views
from . import views


urlpatterns = [
    path("", views.ApartmentList.as_view(), name="home"),
    path("search", views.SearchApartment.as_view()),
    path("guest", views.hello_guest),
    path("<str:kapt_name>-<int:pk>/", views.ApartmentDetail.as_view()),
    path("<str:kapt_name>/feed/", include("feeds.urls")),
    path("<str:kapt_name>/notice/", include("notices.urls")),
    path("<str:kapt_name>/contact/", include("contacts.urls")),
    path("<str:kapt_name>/schedule/", include("schedule.urls")),
    path("<str:kapt_name>/complaint/", include("complaints.urls")),
    path("<str:kapt_name>/poll/", include("polls.urls")),
    # path(
    #    "<str:kapt_name>/profile/myprofile",
    #    users_views.MyProfile.as_view(),
    #    name="my_profile",
    # ),
    # path(
    #    "<str:kapt_name>/profile/@<str:username>",
    #    users_views.PublicUserProfile.as_view(),
    #    name="public_profile",
    # ),
]
