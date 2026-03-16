from rest_framework import permissions

class IsEditorOrAuthorReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow editors to approve articles.
    Journalists can create/edit their own, but cannot change 'is_approved'.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is an Editor
        if request.user.role == 'editor':
            return True

        # Authors can edit their own work, but we handle the 'is_approved' 
        # restriction in the serializer or viewset.
        return obj.author == request.user and request.user.role == 'journalist'