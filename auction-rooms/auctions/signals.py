import json

from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from auctioneer.auctions.models import Bid, Auction
from auctioneer.auctions.serializers import BidSerializer, \
    PublicAuctionSerializer
from auctioneer.auctions.tasks import send_new_listing_notifications
from auctioneer.emailer import tasks
from auctioneer.event_log.models import EventLog

auction_completed = Signal(providing_args=['auction'])


@receiver(post_save, sender=Auction)
def auction_save(sender, instance, created, **kwargs):
    """
    Auction post save handler
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created and not kwargs['raw']:
        EventLog.objects.log_auction_created(instance)
        send_new_listing_notifications.delay(instance.id)


@receiver(post_save, sender=Bid)
def bid_save(sender, instance, created, **kwargs):
    """
    Bid post save handler
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created and not kwargs['raw']:
        # Send the auction owner a copy of the new bid via channels
        instance.auction.send_provider_message({
            'text': json.dumps(BidSerializer(instance).data)
        })

        # Send any public watchers the updated auction data
        instance.auction.send_public_message({
            'text': json.dumps(PublicAuctionSerializer(instance.auction).data)
        })

        EventLog.objects.log_bid_placed(instance)
        EventLog.objects.log_placed_bid(instance)


@receiver(auction_completed, sender=Auction)
def auction_post_complete(sender, auction, **kwargs):
    """
    Auction complete signal handler
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    EventLog.objects.log_auction_ended(auction)
    if auction.was_won():
        # Send the winner an email
        EventLog.objects.log_won_auction(auction)
        tasks.guest_auction_won.delay(
            recipient_id=auction.highest_bid().user.id,
            auction_id=auction.id
        )
    else:
        # Send the loser (if any) an email
        highest_bid = auction.highest_bid()
        if highest_bid is not None:
            EventLog.objects.log_lost_auction(auction)
            tasks.guest_auction_lost.delay(
                recipient_id=auction.highest_bid().user.id,
                auction_id=auction.id
            )

    tasks.provider_auction_finished.delay(
        recipient_id=auction.experience.user.id,
        auction_id=auction.id
    )
