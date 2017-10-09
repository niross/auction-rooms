from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ExperiencesView.as_view(),
        name='experiences'
    ),
]
