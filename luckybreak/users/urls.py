from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^dashboard/$',
        view=views.DashboardView.as_view(),
        name='dashboard'
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
]
