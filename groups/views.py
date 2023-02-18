from django.db import transaction
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status, mixins, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Group, Membership
from .permissions import CanEditMembers, CanEditGroup
from .serializers import GroupSerializer, MemberSerializer
from users.models import User


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, CanEditGroup]

    def get_queryset(self):
        return self.request.user.group_set

class GroupView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.group_set

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class MemberDetailView(mixins.DestroyModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.CreateModelMixin,
                              generics.GenericAPIView):

    permission_classes=[IsAuthenticated, CanEditMembers]
    serializer_class = MemberSerializer

    def get_queryset(self):
        return self.request.user.group_set
    
    def get_object(self, queryset=None):
        ser = MemberSerializer(data=self.request.data)
        if(ser.is_valid()):
            vd = ser.validated_data
            ser.ensure_user_id_exists(vd)
            print(vd)
            membership = get_object_or_404(User, pk=vd["user_id"]).membership_set.get(group_id=vd["group_id"])
            self.check_object_permissions(self.request, membership)
            return membership
        raise serializers.ValidationError(ser.error_messages)

    def post(self, request, *args, **kwargs): 
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)