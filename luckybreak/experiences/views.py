from django.views.generic import ListView, DetailView

from luckybreak.common.mixins import UserIsProviderMixin
from . import models


class ExperiencesView(UserIsProviderMixin, ListView):
    model = models.Experience
    template_name = 'experiences/experiences.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super(ExperiencesView, self).get_queryset()
        return qs.filter(user=self.request.user, deleted=False)


class ExperienceView(UserIsProviderMixin, DetailView):
    model = models.Experience
    template_name = 'experiences/experiences.html'

    def get_queryset(self):
        qs = super(ExperienceView, self).get_queryset()
        return qs.filter(user=self.request.user, deleted=False)
