# posts/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit/delete it.
    Read-only requests are allowed for any user.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for owner (assumes object has `author` attribute)
        return getattr(obj, 'author', None) == request.user
