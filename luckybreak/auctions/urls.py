from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ProviderAuctionsView.as_view(),
        name='provider-auctions'
    ),
]
