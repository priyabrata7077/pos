from rest_framework import permissions

class IsNotEmployee(permissions.BasePermission):
    """
    Custom permission to check if the user is not an employee.
    """

    def has_permission(self, request, view):
        return not request.user.is_employee
