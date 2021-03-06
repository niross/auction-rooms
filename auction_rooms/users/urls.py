from django.conf.urls import url
from django.views import defaults as default_views

from . import views

app_name = 'users'

urlpatterns = [
    url(
        regex=r'^dashboard/$',
        view=views.DashboardView.as_view(),
        name='dashboard'
    ),
    url(
        regex=r'^dashboard/settings/$',
        view=views.SettingsView.as_view(),
        name='settings'
    ),
    url(
        regex=r'^accounts/signup/guest/$',
        view=views.GuestSignupView.as_view(),
        name='guest-signup'
    ),
    url(
        regex=r'^accounts/signup/provider/$',
        view=views.ProviderSignupView.as_view(),
        name='provider-signup'
    ),
    url(
        regex=r'^accounts/signup/$',
        view=default_views.page_not_found,
        kwargs={'exception': Exception('Page not Found')}
    ),
]
