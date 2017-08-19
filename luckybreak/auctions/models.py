from __future__ import unicode_literals
from datetime import datetime
import pytz

from django.db import models

from luckybreak.common.models import DeletableTimeStampedModel
from luckybreak.experiences.models import Experience
from luckybreak.users.models import User


class Auction(DeletableTimeStampedModel):
    experience = models.ForeignKey(Experience, related_name='auctions')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateTimeField()
    view_count = models.PositiveIntegerField(default=0)
    search_appearance_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return '{}, {}, ending {}'.format(
            self.experience.title,
            self.formatted_current_price(),
            self.end_date
        )

    def is_live(self):
        """
        Return whether the auction is still biddable
        """
        return self.end_date > datetime.utcnow().replace(tzinfo=pytz.utc)

    def status(self):
        if self.is_live():
            return 'Live'
        return 'Complete'

    def highest_bid(self):
        if self.bids.count() > 0:
            return self.bids().order_by('-price').first()
        return None

    def current_price(self):
        bid = self.highest_bid()
        if bid is not None:
            return bid.price
        return self.starting_price

    def formatted_current_price(self):
        return '{}{}'.format(
            self.experience.currency.symbol,
            self.current_price()
        )


class Bid(DeletableTimeStampedModel):
    auction = models.ForeignKey(Auction, related_name='bids')
    user = models.ForeignKey(User, related_name='bids')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('-price',)

    def __unicode__(self):
        return '{} bid on {} from {}'.format(
            self.formatted_price(),
            self.auction.experience.name,
            self.user.get_full_name()
        )

    def formatted_price(self):
        return '{}{}'.format(
            self.auction.experience.currency.symbol,
            self.price
        )
