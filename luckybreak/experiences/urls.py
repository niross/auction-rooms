from django.conf.urls import url
from django.views import defaults as default_views

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ExperiencesView.as_view(),
        name='experiences'
    ),
]
