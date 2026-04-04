from rest_framework.permissions import BasePermission
from .models import UserRole


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.ADMIN


class IsHQManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            UserRole.ADMIN, UserRole.HQ_MANAGER
        ]


class IsBranchManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            UserRole.ADMIN, UserRole.HQ_MANAGER, UserRole.BRANCH_MANAGER
        ]


class IsAccountant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            UserRole.ADMIN, UserRole.HQ_MANAGER, UserRole.ACCOUNTANT
        ]


class IsPompiste(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            UserRole.ADMIN, UserRole.BRANCH_MANAGER, UserRole.POMPISTE
        ]


class IsHQStaff(BasePermission):
    """HQ Manager, Accountant, or Admin."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            UserRole.ADMIN, UserRole.HQ_MANAGER, UserRole.ACCOUNTANT
        ]


class IsBranchOrAbove(BasePermission):
    """Branch Manager or above."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            UserRole.ADMIN, UserRole.HQ_MANAGER, UserRole.ACCOUNTANT, UserRole.BRANCH_MANAGER
        ]
