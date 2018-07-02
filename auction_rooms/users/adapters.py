from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from auction_rooms.users import models

class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def save_user(self, request, user, form, commit=False):
        user = super(AccountAdapter, self).save_user(request, user, form, commit=False)
        data = form.cleaned_data
        user.user_type = data.get('user_type')
        if user.user_type == models.User.USER_TYPE_PROVIDER:
            user.phone = data.get('phone')
        user.save()
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
