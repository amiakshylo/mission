
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from user_management.models import UserProfile


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of a user profile or admins to access the related roles,
    with type checking for the user_profile_pk parameter.
    """

    def has_permission(self, request, view):
        user_profile_pk = view.kwargs.get('user_profile_pk')

        # Ensure that user_profile_pk is an integer
        if not isinstance(user_profile_pk, int):
            try:
                user_profile_pk = int(user_profile_pk)
            except ValueError:
                raise PermissionDenied("Invalid user profile ID.")

        # Get the user profile object
        try:
            user_profile = UserProfile.objects.get(pk=user_profile_pk)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("User profile not found.")

        # Attach the user profile to the view for use in has_object_permission
        view.user_profile = user_profile

        # Check if the user is an admin
        if request.user and request.user.is_staff:
            return True

        # Check if the user is the owner of the user profile
        if user_profile.user.id == request.user.id:
            return True

        # Deny permission if the user is not an admin or the owner
        raise PermissionDenied("You do not have permission to view these roles.")

    def has_object_permission(self, request, view, obj):
        # This function may not be needed if has_permission already covers the necessary checks.
        return True
