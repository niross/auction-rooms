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
    url(
        regex=r'^auction/(?P<pk>[0-9]+)/$',
        view=views.ProviderAuctionView.as_view(),
        name='provider-auction'
    ),
    url(
        regex=r'^(?P<pk>[0-9]+)/$',
        view=views.AuctionView.as_view(),
        name='public-auction'
    ),
    url(
        regex=r'^favourites/$',
        view=views.FavouritesView.as_view(),
        name='favourites'
    ),
]
