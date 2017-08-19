from django import forms
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import LoginForm, SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm

from luckybreak.users import models


class LBLoginForm(LoginForm):
    error_messages = {
        'account_inactive': _(
            "This account is currently inactive."
        ),
        'email_password_mismatch': _(
            "We didn't recognise that email/password."
        ),
        'username_password_mismatch': _(
            "We didn't recognise that email/password."
        ),
        'username_email_password_mismatch': _(
            "We didn't recognise that email/password."
        )
    }


class LBSignupForm(SignupForm):
    _USER_TYPE_CHOICES = (
        (models.User.USER_TYPE_GUEST, 'I\'m looking for experiences'),
        (models.User.USER_TYPE_PROVIDER, 'I\'m selling experiences'),
    )
    user_type = forms.ChoiceField(choices=_USER_TYPE_CHOICES)
    phone = forms.CharField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(LBSignupForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            if 'user_type' in kwargs['initial']:
                self.fields['user_type'].widget = forms.widgets.HiddenInput(attrs={
                    'hidden': True
                })
                if kwargs['initial']['user_type'] == models.User.USER_TYPE_GUEST:
                    self.fields['phone'].widget = forms.widgets.HiddenInput(attrs={
                        'hidden': True
                    })


class LBSocialSignupForm(SocialSignupForm):
    _USER_TYPE_CHOICES = (
        (models.User.USER_TYPE_GUEST, 'I\'m looking for experiences'),
        (models.User.USER_TYPE_PROVIDER, 'I\'m selling experiences'),
    )
    user_type = forms.ChoiceField(choices=_USER_TYPE_CHOICES)
    phone = forms.CharField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(LBSocialSignupForm, self).__init__(*args, **kwargs)
        if 'data' in kwargs and kwargs['data']['user_type'] == models.User.USER_TYPE_PROVIDER:
            self.fields['phone'].required = True
