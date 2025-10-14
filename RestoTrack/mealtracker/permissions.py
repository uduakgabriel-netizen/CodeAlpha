from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to superusers (site admin).
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsStaffOrAdmin(permissions.BasePermission):
    """
    Allows access to users with is_staff True or superusers.
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_staff or user.is_superuser))
