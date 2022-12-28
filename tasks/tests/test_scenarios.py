import pytest
from django.urls import reverse
from tasks.models import *


def test_create_normal_task(db, new_authenticated_client_user, new_list):
    client, user = new_authenticated_client_user()
    list = new_list(user)

    client.post(reverse("create_taks"), {
        "title": "new task",
        "notes": "some notes",
        "list": list.id
    })

    assert Task.objects.count() == 1



# def test_create_super_task():
#     pass


# def test_create_normal_repetitive_task():
#     pass


# def test_create_super_repetitive_task():
#     pass


# def test_finish_task():
#     pass


# def test_finish_repetitive_task():
#     pass
