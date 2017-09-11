from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from allauth.account.views import SignupView

from luckybreak.users import models


class DashboardView(LoginRequiredMixin, TemplateView):
    provider_template_name = 'users/provider_dashboard.html'
    guest_template_name = 'users/guest_dashboard.html'

    def get_context_data(self, **kwargs):
        return super(DashboardView, self).get_context_data(**kwargs)

    def get_template_names(self):
        if self.request.user.is_provider():
            return [self.provider_template_name]
        return [self.guest_template_name]


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
