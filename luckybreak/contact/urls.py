from django.conf.urls import url

from luckybreak.contact import views
from luckybreak.contact import signals

urlpatterns = [
    url(r'^$', view=views.ContactView.as_view(), name='contact'),
]
