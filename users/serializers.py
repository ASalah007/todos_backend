from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .emails import send_verification_email
from .models import User, UserToken
from tasks.models import List
from django.db import transaction 



class UserSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        return make_password(value)


    @transaction.atomic
    def create(self, validated_data):
        user = super().create(validated_data)
        a = List.objects.create(title="assigned", user=user)
        d = List.objects.create(title="default", user=user)
        user.default_list_id = a.id
        user.assigned_list_id = d.id
        user.save()
        token = UserToken.objects.create(user=user).token
        send_verification_email(
            recipient=user.email,
            message=token,
        )
        return user

    class Meta:
        model = User
        fields = ["id", "name", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
