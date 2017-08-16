from django.conf.urls import url

from luckybreak.browse import views

urlpatterns = (
    url(
        r'^$',
        views.HomepageView.as_view(),
        name='homepage'
    ),
)
