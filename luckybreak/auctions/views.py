from django.views.generic import ListView

from luckybreak.common.mixins import UserIsProviderMixin
from . import models


class ProviderLiveAuctionsView(UserIsProviderMixin, ListView):
    model = models.Auction
    template_name = 'auctions/provider_live_auctions.html'
    paginate_by = 10

    def get_queryset(self):
        return models.Auction.objects.live().filter(
            experience__user=self.request.user,
        ).order_by('end_date')


class ProviderFinishedAuctionsView(UserIsProviderMixin, ListView):
    model = models.Auction
    template_name = 'auctions/provider_finished_auctions.html'
    paginate_by = 10

    def get_queryset(self):
        return models.Auction.objects.finished().filter(
            experience__user=self.request.user
        ).order_by('-end_date')
