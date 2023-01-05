from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Group, Membership
from users.models import User
from .serializers import GroupSerializer
from .permissions import CanAddMembers


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(members=self.request.user)

class GroupView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.group_set

    def post(self, request, *args, **kwargs):
        print(request.data)
        self.get_serializer()
        return super().post(request, *args, **kwargs)


class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, CanAddMembers]


    def get_queryset(self):
        group_id = self.request.parser_context.get('kwargs').get("group_id")
        group = get_object_or_404(Group, pk=group_id)
        return group.users

