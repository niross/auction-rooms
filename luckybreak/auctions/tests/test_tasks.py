from datetime import datetime, timedelta

import mock
import pytz

from luckybreak.auctions.models import Auction, Bid
from luckybreak.auctions.tasks import increment_search_appearance_count, \
    increment_view_count, complete_auctions
from luckybreak.common.tests import BaseTestCase


class AuctionTasksTestCase(BaseTestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json', 'auctions.json'
    ]

    @mock.patch('luckybreak.auctions.signals.auction_completed.send')
    def test_complete_auctions(self, signal):
        auction = Auction.objects.get(pk=1)
        Bid.objects.create(
            user=self.guest,
            auction=auction,
            price=auction.reserve_price + 1
        )
        auction.end_date = datetime.now(pytz.UTC) - timedelta(hours=1)
        auction.save()
        complete_auctions()

        self.assertTrue(signal.called)

    @mock.patch('luckybreak.auctions.signals.auction_completed.send')
    def test_no_complete_auctions(self, signal):
        complete_auctions()
        self.assertFalse(signal.called)

    def test_increment_search_appearance_count(self):
        searches = Auction.objects.get(pk=1).search_appearance_count
        increment_search_appearance_count([1])
        self.assertEqual(
            Auction.objects.get(pk=1).search_appearance_count,
            searches + 1
        )

    def test_increment_view_count(self):
        views = Auction.objects.get(pk=1).view_count
        increment_view_count(1)
        self.assertEqual(
            Auction.objects.get(pk=1).view_count,
            views + 1
        )
