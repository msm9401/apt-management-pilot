"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path("", include("django_prometheus.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/houses/", include("houses.urls")),
    path("api/v1/users/", include("users.urls")),
    # path("__debug__/", include("debug_toolbar.urls")),
    path("convert/", include("guest_user.urls")),
]

admin.site.site_header = "아파트 관리"
admin.site.site_title = "아파트 관리"
admin.site.index_title = "백오피스"
admin.site.site_url = "/admin/"

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
