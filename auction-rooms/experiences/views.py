from django.views.generic import ListView

from auctioneer.common.mixins import UserIsProviderMixin
from . import models


class ExperiencesView(UserIsProviderMixin, ListView):
    model = models.Experience
    template_name = 'experiences/experiences.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super(ExperiencesView, self).get_queryset()
        return qs.filter(user=self.request.user, deleted=False)

    def get_context_data(self, **kwargs):
        context = super(ExperiencesView, self).get_context_data(**kwargs)

        # Show the experience feature discovery on the first page view
        user = self.request.user
        context['show_experience_help'] = user.show_experience_help
        if context['show_experience_help']:
            user.show_experience_help = False
            user.save()

        return context

