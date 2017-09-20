from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from luckybreak.common.mixins import UserIsProviderMixin
from . import models


class ProviderLiveAuctionsView(UserIsProviderMixin, ListView):
    model = models.Auction
    template_name = 'auctions/provider_live_auctions.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super(ProviderLiveAuctionsView, self).get_queryset()
        return qs.filter(
            experience__user=self.request.user,
            deleted=False
        ).order_by('end_date')


class ProviderFinishedAuctionsView(UserIsProviderMixin, ListView):
    model = models.Auction
    template_name = 'auctions/provider_finished_auctions.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super(ProviderFinishedAuctionsView, self).get_queryset()
        return qs.filter(
            experience__user=self.request.user,
            deleted=False,
            end_date__lt=datetime.utcnow()
        ).order_by('-end_date')
