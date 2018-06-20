from django.conf.urls import url

from auctioneer.browse import views

urlpatterns = (
    url(
        r'^$',
        views.HomepageView.as_view(),
        name='homepage'
    ),
    url(
        r'^start-listing/$',
        views.ProviderMarketingView.as_view(),
        name='provider-marketing'
    ),
    url(
        r'^search/$',
        views.SearchResultsView.as_view(),
        name='search-results'
    ),
)
