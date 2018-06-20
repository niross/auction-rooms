from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.contrib import messages

from allauth.account.views import SignupView

from auctioneer.users import models


class DashboardView(LoginRequiredMixin, TemplateView):
    provider_template_name = 'users/provider_dashboard.html'
    guest_template_name = 'users/guest_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        # Show auction the welcome message if it hasn't already
        # been shown.
        user = self.request.user
        context['show_dashboard_welcome'] = user.show_dashboard_welcome
        if context['show_dashboard_welcome']:
            user.show_dashboard_welcome = False
            user.save()

        return context


    def get_template_names(self):
        if self.request.user.is_provider():
            return [self.provider_template_name]
        return [self.guest_template_name]


class SettingsView(LoginRequiredMixin, UpdateView):
    model = models.User
    template_name = 'users/settings.html'
    fields = ['first_name', 'last_name', 'email', 'phone']

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your settings were updated successfully')
        return super(SettingsView, self).form_valid(form)

    def get_success_url(self):
        return reverse('users:settings')


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
