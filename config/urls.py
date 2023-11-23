from django.contrib import admin
from django.urls import path, include, re_path

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/drf-auth/", include('rest_framework.urls')),
    path("api/v1/auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("api/v1/", include("book_reading.urls")),
]

urlpatterns += doc_urls