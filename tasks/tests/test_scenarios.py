import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    "title, due_date, finished_date, start_date, notes, list, is_super, super_task_id",
     [ 
        ("cook a meal", "", "", "", "", "1", )
     ]
)
def test_create_normal_task(db, new_authenticated_client_user, new_list):
    client, user = new_authenticated_client_user()
    new_list(user)

    client.post(reverse("create_taks"), {})



def test_create_super_task():
    pass


def test_create_normal_repetitive_task():
    pass


def test_create_super_repetitive_task():
    pass


def test_finish_task():
    pass


def test_finish_repetitive_task():
    pass
