from django.shortcuts import render
from django.views.generic import ListView, DetailView

from luckybreak.common.mixins import UserIsProviderMixin
from . import models


class ProviderAuctionsView(UserIsProviderMixin, ListView):
    model = models.Auction
    template_name = 'auctions/provider_auctions.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super(ProviderAuctionsView, self).get_queryset()
        return qs.filter(experience__user=self.request.user, deleted=False)
