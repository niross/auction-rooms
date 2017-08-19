from django.conf.urls import url

from luckybreak.browse import views

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
)
