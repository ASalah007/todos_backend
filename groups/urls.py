from django.urls import path
from .views import *


urlpatterns = [
    path("create/", GroupView.as_view(), name="group_create"),
    path("list/", GroupView.as_view(), name="group_list"),
    path("<int:pk>/", GroupDetailView.as_view(), name="group_detail"),
    path("member/", MemberDetailView.as_view(), name="member_detail"),
    # path("member/<int:group_id>/", MemberAddRemoveView.as_view(), name="members"),
]

