from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .emails import send_verification_email
from .models import User, UserToken


class UserSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        return make_password(value)

    def create(self, validated_data):
        user = super().create(validated_data)
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
