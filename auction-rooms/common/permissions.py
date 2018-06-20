from rest_framework import permissions

from auctioneer.users.models import User


class IsGuestPerm(permissions.IsAuthenticated):
    """
    Allow access to guests only
    """
    def has_permission(self, request, view):
        return super(IsGuestPerm, self).has_permission(request, view) \
                and request.user.user_type == User.USER_TYPE_GUEST


class IsProviderPerm(permissions.IsAuthenticated):
    """
    Allow access to providers only
    """
    def has_permission(self, request, view):
        return super(IsProviderPerm, self).has_permission(request, view) \
                and request.user.user_type == User.USER_TYPE_PROVIDER
