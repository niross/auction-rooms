from django.conf.urls import url

from auctioneer.contact import views
from auctioneer.contact import signals

urlpatterns = [
    url(r'^$', view=views.ContactView.as_view(), name='contact'),
]
