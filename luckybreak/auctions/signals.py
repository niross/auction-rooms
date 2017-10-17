import json

from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from luckybreak.auctions.models import Bid, Auction
from luckybreak.auctions.serializers import BidSerializer, \
    PublicAuctionSerializer
from luckybreak.event_log.models import EventLog

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
    if created:
        EventLog.objects.log_auction_created(instance)


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
    if created:
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
