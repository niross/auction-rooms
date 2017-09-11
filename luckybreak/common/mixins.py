from django.contrib.auth.mixins import UserPassesTestMixin

from luckybreak.users.models import User


class UserIsGuestMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated() \
                and self.request.user.user_type == User.USER_TYPE_GUEST


class UserIsProviderMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated() \
                and self.request.user.user_type == User.USER_TYPE_PROVIDER
