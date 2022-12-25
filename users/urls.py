from django.urls import path
from .views import *

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user_create"),
    path("verify/<str:token>/", UserVerifyView.as_view(), name="user_verify"),
    path(
        "reset_password/",
        ResetPasswordRequestView.as_view(),
        name="reset_password_request",
    ),
    path(
        "reset_password/<str:token>/",
        ResetPasswordView.as_view(),
        name="reset_password",
    ),
    path("detail/", UserDetailView.as_view(), name="user_detail")
]
