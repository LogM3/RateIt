from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права доступа для категорий, жанров и произведений."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_superuser
            )
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_superuser
        )


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Права доступа для отзывов и комментариев."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.is_superuser
        )
