from django.conf.urls import url

from . import views

app_name = 'experiences'

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ExperiencesView.as_view(),
        name='experiences'
    ),
]
