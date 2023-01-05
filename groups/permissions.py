from django.shortcuts import get_object_or_404
from .models import Group, Membership
from rest_framework.permissions import BasePermission


class CanAssignTasks(BasePermission):
    def has_object_permission(self, request, view, group_id):
        membership = get_object_or_404(Membership, member=request.user, group_id=group_id)
        if membership.can_assign_tasks:
            return True 

        return False 

class CanEditGroup(BasePermission):
    def has_object_permission(self, request, view, group_id):
        membership = get_object_or_404(member=request.user, group_id=group_id)
        if membership.can_edit_group:
            return True 

        return False 

class CanAddMembers(BasePermission):
    def has_object_permission(self, request, view, group_id):
        membership = get_object_or_404(member=request.user, group_id=group_id)
        if membership.can_add_members:
            return True 

        return False 
