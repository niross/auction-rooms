from django.conf.urls import url

from auction_rooms.contact import views
from auction_rooms.contact import signals

app_name = 'contact'

urlpatterns = [
    url(r'^$', view=views.ContactView.as_view(), name='contact'),
]
