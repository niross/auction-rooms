from datetime import datetime, timedelta

import mock
import pytz
from dateutil.relativedelta import relativedelta
from django.core import mail

from luckybreak.auctions.models import Auction, Bid, Favourite
from luckybreak.auctions.tasks import increment_search_appearance_count, \
    increment_view_count, complete_auctions
from luckybreak.common.tests import BaseTestCase
from luckybreak.emailer.models import EmailLog


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

    def test_complete_auction_emails_sent(self):
        # Provider complete and guest loser emails should be sent
        outbox_count = len(mail.outbox)
        auction = Auction.objects.get(pk=1)
        Bid.objects.create(
            user=self.guest,
            auction=auction,
            price=auction.reserve_price - 1
        )
        auction.end_date = datetime.now(pytz.UTC) - timedelta(hours=1)
        auction.save()
        complete_auctions()
        self.assertEqual(len(mail.outbox), outbox_count + 2)

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


class NewListingNotificationTestCase(BaseTestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json', 'auctions.json'
    ]

    def setUp(self):
        super(NewListingNotificationTestCase, self).setUp()
        self.auction = Auction.objects.get(pk=1)
        self.experience = self.auction.experience
        self.favourite = Favourite.objects.create(
            auction=self.auction,
            user=self.guest
        )

    # # Test favourited auction has not completed
    # def test_live_favourited_auction(self):
    #     outbox_count = len(mail.outbox)
    #     Auction.objects.create_auction(
    #         self.experience,
    #         datetime.utcnow() + timedelta(days=10),
    #         datetime.utcnow() + timedelta(days=11),
    #         2.00,
    #         3.00,
    #         datetime.utcnow() + timedelta(days=5)
    #     )
    #     self.assertEqual(len(mail.outbox), outbox_count)
    #
    # # Test user won favourited auction
    # def test_user_won_favourited_auction(self):
    #     Bid.objects.create(
    #         user=self.guest,
    #         auction=self.auction,
    #         price=self.auction.reserve_price - 1
    #     )
    #     self.auction.end_date = datetime.now(pytz.UTC) - timedelta(hours=1)
    #     self.auction.save()
    #     self.auction.mark_complete()
    #     outbox_count = len(mail.outbox)
    #     Auction.objects.create_auction(
    #         self.experience,
    #         datetime.utcnow() + timedelta(days=10),
    #         datetime.utcnow() + timedelta(days=11),
    #         2.00,
    #         3.00,
    #         datetime.utcnow() + timedelta(days=5)
    #     )
    #     self.assertEqual(len(mail.outbox), outbox_count)

    # Test user received a new listing email already today
    def test_send_one_new_listing_email_per_day(self):
        self.auction.end_date = datetime.now(pytz.UTC) - timedelta(hours=1)
        self.auction.save()
        self.auction.mark_complete()
        outbox_count = len(mail.outbox)
        EmailLog.objects.create(
            recipient=self.guest.email,
            name='Favourited Auction Relisted',
            subject='Test Subject',
            content='This is a dummy email',
        )
        Auction.objects.create_auction(
            self.experience,
            datetime.utcnow() + timedelta(days=10),
            datetime.utcnow() + timedelta(days=11),
            2.00,
            3.00,
            datetime.utcnow() + timedelta(days=5)
        )
        self.assertEqual(len(mail.outbox), outbox_count)

    # Test user already received a new listing email about this favourite
    def test_single_email_sent_per_favourite(self):
        # Complete the auction
        self.auction.end_date = datetime.now(pytz.UTC) - timedelta(hours=1)
        self.auction.save()
        self.auction.mark_complete()

        # Mark the new listing email as sent
        self.favourite.new_listing_sent = True
        self.favourite.save()

        outbox_count = len(mail.outbox)

        # Create a new auction from the same experience
        Auction.objects.create_auction(
            self.experience,
            datetime.utcnow() + timedelta(days=10),
            datetime.utcnow() + timedelta(days=11),
            2.00,
            3.00,
            datetime.utcnow() + timedelta(days=5)
        )

        # No email should be sent
        self.assertEqual(len(mail.outbox), outbox_count)

    # Test favourited auction finished over 6 months ago
    def test_no_spam_on_old_favourites(self):
        # Complete the auction (9 months ago)
        self.auction.end_date = datetime.now(pytz.UTC) - relativedelta(months=9)
        self.auction.save()
        self.auction.mark_complete()

        outbox_count = len(mail.outbox)

        # Create a new auction from the same experience
        Auction.objects.create_auction(
            self.experience,
            datetime.utcnow() + timedelta(days=10),
            datetime.utcnow() + timedelta(days=11),
            2.00,
            3.00,
            datetime.utcnow() + timedelta(days=5)
        )

        # No email should be sent
        self.assertEqual(len(mail.outbox), outbox_count)

    # Test send notification
    def test_send_new_listing_notification(self):
        # Complete the auction
        self.auction.end_date = datetime.now(pytz.UTC) - timedelta(hours=1)
        self.auction.save()
        self.auction.mark_complete()

        outbox_count = len(mail.outbox)

        # Create a new auction from the same experience
        Auction.objects.create_auction(
            self.experience,
            datetime.utcnow() + timedelta(days=10),
            datetime.utcnow() + timedelta(days=11),
            2.00,
            3.00,
            datetime.utcnow() + timedelta(days=5)
        )

        # 1 email should be sent
        self.assertEqual(len(mail.outbox), outbox_count + 1)

        # The favourite should be marked as 'new listing email sent'
        fav = Favourite.objects.get(pk=self.favourite.id)
        self.assertTrue(fav.new_listing_sent)


