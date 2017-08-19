from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from allauth.account.views import SignupView

from luckybreak.users import models


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'


class GuestSignupView(SignupView):
    def get_initial(self):
        initial = super(GuestSignupView, self).get_initial()
        initial['user_type'] = models.User.USER_TYPE_GUEST
        return initial


class ProviderSignupView(SignupView):
    def get_initial(self):
        initial = super(ProviderSignupView, self).get_initial()
        initial['user_type'] = models.User.USER_TYPE_PROVIDER
        return initial
