from django.urls import path
from .views import *


urlpatterns = [
    path("create/", GroupView.as_view(), name="group_create"),
    path("list/", GroupView.as_view(), name="group_list"),
    # path("member/<int:group_id>/", MemberAddRemoveView.as_view(), name="members"),
]

