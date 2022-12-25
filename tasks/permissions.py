from rest_framework.permissions import BasePermission


class IsTaskOwner(BasePermission):
    def has_object_permission(self, request, view, task):
        if request.user == task.user:
            return True

        return False
