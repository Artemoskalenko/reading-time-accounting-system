from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/swagger/")),
    path("drf-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("api/v1/", include("book_reading.urls")),
]

urlpatterns += doc_urls
