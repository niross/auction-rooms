from datetime import datetime, timedelta

import pytz
from django.core import mail

from luckybreak.auctions.models import Auction, Bid
from luckybreak.common.tests import BaseTestCase


class AuctionModelTestCase(BaseTestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json', 'auctions.json'
    ]

    def test_complete_auction_sold(self):
        auction = Auction.objects.get(pk=1)
        Bid.objects.create(
            user=self.guest,
            auction=auction,
            price=auction.reserve_price + 1
        )
        auction.end_date = datetime.now(pytz.UTC) - timedelta(hours=1)
        auction.save()
        provider_events = self.provider.events.count()
        guest_events = self.guest.events.count()
        auction.mark_complete()
        self.assertEqual(self.provider.events.count(), provider_events + 1)
        self.assertEqual(self.guest.events.count(), guest_events + 1)
        self.assertEqual(len(mail.outbox), 2)

    def test_complete_auction_unsold(self):
        auction = Auction.objects.get(pk=1)
        auction.end_date = datetime.now(pytz.UTC) - timedelta(hours=1)
        auction.save()
        events = self.provider.events.count()
        auction.mark_complete()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(self.provider.events.count(), events + 1)
