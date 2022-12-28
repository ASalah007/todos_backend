import factory
from factory.django import DjangoModelFactory
from ..models import *
from faker import Faker
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    name = fake.name()
    email = fake.email()
    password = make_password("123")
    created_at = fake.date_time()
    last_login = fake.date_time()
    is_staff = False
    is_active = True


class ListFactory(DjangoModelFactory):
    class Meta:
        model = List

    title = fake.word()
    user = factory.SubFactory(UserFactory)


class RepetitiveTaskInfoFactory(DjangoModelFactory):
    class Meta:
        model = Task

    title = fake.word()
    due_date = fake.date_time()
    finished_date = fake.date_time()
    start_date = fake.date()
    notes = fake.text()
    list = factory.SubFactory(ListFactory)
    user = factory.SubFactory(UserFactory)
    is_super = fake.boolean()


class RepetitiveTaskFactory(DjangoModelFactory):
    class Meta: 
        model = RepetitiveTask

    repetitive_task_info = factory.SubFactory(RepetitiveTaskInfoFactory)
    finished_date = fake.date_time()
    start_date = fake.date()
    notes = fake.text()


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    title = fake.name()
    due_date = fake.date_time()
    user = factory.SubFactory(UserFactory)
    list = factory.SubFactory(ListFactory)
    start_date = fake.date_time()
    notes = fake.text()
    user = factory.SubFactory(UserFactory)
    list = factory.SubFactory(ListFactory)
    is_super = fake.boolean()
