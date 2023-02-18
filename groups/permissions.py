from django.shortcuts import get_object_or_404
from .models import Group, Membership
from rest_framework.permissions import BasePermission


class CanAssignTasks(BasePermission):
    def has_object_permission(self, request, view, membership):
        return membership.can_assign_tasks
    
class CanEditGroup(BasePermission):
    def has_object_permission(self, request, view, group):
        user_membership = request.user.membership_set.get(group_id=group.id)
        return user_membership.can_edit_group

class CanEditMembers(BasePermission):
    def has_object_permission(self, request, view, member):
        user_membership = request.user.membership_set.get(group_id=request.data["group_id"])
        can_remove_member = member.role >= user_membership.role
        return user_membership.can_add_members and can_remove_member