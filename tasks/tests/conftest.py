import pytest
from django.urls import reverse
from pytest_factoryboy import register
from .factories import *
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

register(RepetitiveTaskInfoFactory)
register(RepetitiveTaskFactory)
register(ListFactory)
register(UserFactory)
register(TaskFactory)


@pytest.fixture
def authenticate(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixutre
def new_authenticated_client_user(user_factory):
    user = user_factory.build()
    return (authenticate(user), user)

@pytest.fixture
def new_list(user, list_factory):
    list = list_factory.create()
    if user:
        list.user = user 
    list.save()
    return list