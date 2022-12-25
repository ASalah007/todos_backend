from django.urls import include, path

from .views import *

urlpatterns = [
    path("all/", UserAllTaskslView.as_view(), name="user_all_tasks"),
    path("create/", TaskCreateView.as_view(), name="create_task"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task_details"),
    path(
        "repetitive/create/",
        RepetitiveTaskInfoCreateView.as_view(),
        name="create_repetitive_task",
    ),
    path(
        "repetitive/info/<int:pk>/",
        RepetitiveTaskInfoDetailView.as_view(),
        name="repetitive_task_info_details",
    ),
    path(
        "repetitive/<int:pk>/",
        RepetitiveTaskEditView.as_view(),
        name="repetitive_task_details",
    ),
    path("list/create", ListCreateView.as_view(), name="create_list"),
]
