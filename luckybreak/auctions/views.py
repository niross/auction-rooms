from django.views.generic import ListView, DetailView

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

    def get_context_data(self, **kwargs):
        context = super(ProviderLiveAuctionsView, self).get_context_data(
            **kwargs
        )

        # Show auction feature discovery if the user has at least one
        # experience, no auctions and has not seen it before
        user = self.request.user
        if user.show_auction_help and user.experiences.exists():
            context['show_auction_help'] = not user.auctions().exists()
            user.show_auction_help = False
            user.save()

        return context


class ProviderFinishedAuctionsView(UserIsProviderMixin, ListView):
    model = models.Auction
    template_name = 'auctions/provider_finished_auctions.html'
    paginate_by = 10

    def get_queryset(self):
        return models.Auction.objects.finished().filter(
            experience__user=self.request.user
        ).order_by('-end_date')


class ProviderAuctionView(UserIsProviderMixin, DetailView):
    model = models.Auction
    context_object_name = 'auction'
    template_name = 'auctions/provider_auction.html'
