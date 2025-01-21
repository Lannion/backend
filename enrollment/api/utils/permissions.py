from rest_framework.permissions import BasePermission
from django.apps import apps


class GroupPermission(BasePermission):
    """
    Custom permission class with granular permissions for groups on specific models and HTTP methods.
    """

    # Define granular permissions
    MODEL_PERMISSIONS = {
        "admin": {
            "*": ["GET", "POST", "PUT", "DELETE"],
        },
        "registrar": {
            "*": ["GET", "POST", "PUT", "DELETE"],
        },
        "department": {
            "*": ["GET", "POST", "PUT", "DELETE"], 
        },
        "student": {
            "*": ["GET"],
            "user": ["GET", "PUT"],
            "student": ["GET", "PUT"],
        },
    }

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Get the user's groups (converted to lowercase for case-insensitive checks)
        user_groups = [group.lower() for group in request.user.groups.values_list('name', flat=True)]

        # Dynamically get the model name from the view
        model = getattr(view, 'model', None)

        if model is None:
            return False  # Deny if the model is not defined in the view
        
        model_name = model._meta.model_name.lower()

        # Check permissions for each group
        for group in user_groups:
            group_permissions = self.MODEL_PERMISSIONS.get(group, {})
            allowed_methods = group_permissions.get(model_name, group_permissions.get("*", []))

            # If the request method is allowed, grant access
            if request.method in allowed_methods:
                return True

        # Default: deny access
        return False

class isRegistrar(BasePermission):
    def has_permission(self, request, view):
        # Check if the user belongs to the 'registrar' group
        return request.user.is_authenticated and request.user.groups.filter(name='registrar').exists()

class isDepartment(BasePermission):
    def has_permission(self, request, view):
        # Check if the user belongs to the 'registrar' group
        return request.user.is_authenticated and request.user.groups.filter(name='department').exists()

class isStudent(BasePermission):
    def has_permission(self, request, view):
        # Check if the user belongs to the 'registrar' group
        return request.user.is_authenticated and request.user.groups.filter(name='student').exists()
