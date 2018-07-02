from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class User(AbstractUser):
    USER_TYPE_GUEST = 1
    USER_TYPE_PROVIDER = 2
    _USER_TYPE_CHOICES = (
        (USER_TYPE_GUEST, 'Guest'),
        (USER_TYPE_PROVIDER, 'Provider'),
    )
    user_type = models.IntegerField(
        choices=_USER_TYPE_CHOICES
    )
    phone = models.CharField(
        max_length=100, null=True, blank=True
    )

    # Feature Discovery
    show_dashboard_welcome = models.BooleanField(default=True)
    show_experience_help = models.BooleanField(default=True)
    show_auction_help = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name()

    def is_provider(self):
        return self.user_type == self.USER_TYPE_PROVIDER

    def auctions(self):
        from auction_rooms.auctions.models import Auction
        return Auction.objects.filter(deleted=False, experience__user=self)

    def live_auctions(self):
        return self.auctions().live()

    def finished_auctions(self):
        return self.auctions().finished()

    def sold_auctions(self):
        return self.auctions().sold()

    def total_live_auctions_by_experience(self):
        return self.live_auctions().distinct('experience').count()

    def total_sold_auctions_by_experience(self):
        return self.sold_auctions().distinct('experience').count()

    def get_favourites(self):
        from auction_rooms.auctions.models import Auction
        return Auction.objects.live().filter(
            id__in=[f.auction.id for f in self.favourites.all()]
        )

    def bid_on_auctions(self):
        from auction_rooms.auctions.models import Auction

        # Find all auctions i've bid on
        return Auction.objects.filter(
            bids__user=self
        ).distinct().order_by('status')

    def won_auctions(self):
        """
        List any auctions this user has won
        :return:
        """
        from auction_rooms.auctions.models import Auction

        # Find all auctions i've bid on
        auctions = Auction.objects.filter(
            status=Auction.STATUS_FINISHED_SOLD,
            bids__user=self
        )
        # Filter them for any i am the highest bidder on
        return Auction.objects.filter(
            pk__in=[a.id for a in auctions if a.highest_bid().user == self]
        )

    def lost_auctions(self):
        """
        List any auctions this user has bid on but not won
        :return:
        """
        from auction_rooms.auctions.models import Auction

        # Find all auctions i've bid on
        auctions = Auction.objects.filter(
            status__in=[
                Auction.STATUS_FINISHED_SOLD,
                Auction.STATUS_FINISHED_UNSOLD
            ],
            bids__user=self
        )
        # Filter them for any i am the highest bidder on
        return Auction.objects.filter(
            pk__in=[a.id for a in auctions if a.highest_bid().user != self]
        )

    def emails(self):
        from auction_rooms.emailer.models import EmailLog
        return EmailLog.objects.filter(recipient=self.email)

