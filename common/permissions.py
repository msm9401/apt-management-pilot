from rest_framework.permissions import IsAdminUser


class IsAdminUserOrAuthenticatedReadOnly(IsAdminUser):

    """
    admin user --> GET, POST, PUT, DELETE
    authenticated user --> GET
    """

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        if not request.user.is_authenticated:
            return False
        return request.method == "GET" or is_admin
