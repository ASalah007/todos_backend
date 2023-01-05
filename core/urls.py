from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path(
        "api/",
        include(
            [
                path(
                    "token/",
                    TokenObtainPairView.as_view(),
                    name="token_obtain_pair",
                ),
                path(
                    "token/refresh/",
                    TokenRefreshView.as_view(),
                    name="token_refresh",
                ),
                path("user/", include("users.urls")),
                path("task/", include("tasks.urls")),
                path("group/", include("groups.urls")),
            ]
        ),
    ),
]