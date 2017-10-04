import json

from django.db.models.signals import post_save
from django.dispatch import receiver

from luckybreak.auctions.models import Bid
from luckybreak.auctions.serializers import BidSerializer


@receiver(post_save, sender=Bid)
def bid_save(sender, instance, created, **kwargs):
    """
    When a bid is created update any listening django channels
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        instance.auction.send_provider_message({
            'text': json.dumps(BidSerializer(instance).data)
        })

