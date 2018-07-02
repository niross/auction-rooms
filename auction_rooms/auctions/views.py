from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from auction_rooms.auctions.tasks import increment_view_count
from auction_rooms.common.mixins import UserIsProviderMixin
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


class AuctionView(DetailView):
    queryset = models.Auction.objects.filter(deleted=False)
    context_object_name = 'auction'
    template_name = 'auctions/auction.html'

    def get_context_data(self, **kwargs):
        context = super(AuctionView, self).get_context_data(**kwargs)
        if not self.request.user.is_staff:
            increment_view_count(context['auction'].id)
        return context


class FavouritesView(LoginRequiredMixin, ListView):
    model = models.Auction
    template_name = 'auctions/favourites.html'
    paginate_by = 10
    context_object_name = 'favourites'

    def get_queryset(self):
        return self.request.user.get_favourites()


class WonAuctionsView(LoginRequiredMixin, ListView):
    model = models.Auction
    template_name = 'auctions/won_auctions.html'
    paginate_by = 10
    context_object_name = 'auctions'

    def get_queryset(self):
        return self.request.user.won_auctions()


class BidsView(LoginRequiredMixin, ListView):
    model = models.Auction
    template_name = 'auctions/bids.html'
    paginate_by = 10
    context_object_name = 'auctions'

    def get_queryset(self):
        return self.request.user.bid_on_auctions()
