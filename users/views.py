from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .emails import send_reset_password_email
from .models import *
from .serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        ser = UserSerializer(request.user)
        return Response(ser.data)

class UserVerifyView(APIView):
    def get(self, request, token):
        user = get_object_or_404(UserToken, token=token).user
        user.is_active = True
        user.save()
        return render(request, "email_verified.html")


class ResetPasswordView(APIView):
    def post(self, request, token):
        user = get_object_or_404(UserToken, token=token).user
        print(request.data["new_password"])
        ser = UserSerializer(
            user, data={"password": request.data["new_password"]}, partial=True
        )
        if ser.is_valid():
            ser.save()
            return Response(
                {"message": "password reset successfully"}, status=status.HTTP_200_OK
            )
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordRequestView(APIView):
    def post(self, request):
        email = request.data["email"]
        try:
            user = User.objects.get(email=email)
        except:
            return Response(
                {"message": "no user with the specified email"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = UserToken.objects.create(user=user).token
        send_reset_password_email(recipient=email, message=token)
        return Response(
            {"message": "please check your email"}, status=status.HTTP_200_OK
        )
