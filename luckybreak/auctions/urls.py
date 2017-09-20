from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^live/$',
        view=views.ProviderLiveAuctionsView.as_view(),
        name='provider-live-auctions'
    ),
    url(
        regex=r'^finished/$',
        view=views.ProviderFinishedAuctionsView.as_view(),
        name='provider-finished-auctions'
    ),
]
