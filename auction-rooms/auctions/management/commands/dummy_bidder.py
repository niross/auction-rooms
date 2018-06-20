import sys

import time
from django.core.management import BaseCommand

from auctioneer.auctions.models import Auction, Bid
from auctioneer.users.models import User


class Command(BaseCommand):
    help = 'Given the id of an auction create the specified number ' \
           '(default 5) of bids in 2 second increments'

    def add_arguments(self, parser):
        parser.add_argument(
            'auction',
            type=int,
            help='The ID of the auction to bid on'
        )
        parser.add_argument(
            'bids',
            type=int,
            help='The number of bids to create'
        )

    def handle(self, *args, **kwargs):
        try:
            auction = Auction.objects.get(pk=kwargs['auction'])
        except Auction.DoesNotExist:
            self.stderr.write('Auction does not exist')
            sys.exit(1)

        guest = User.objects.last()

        for idx in range(1, kwargs['bids'] + 1):
            bid = Bid.objects.create(
                auction=auction,
                user=guest,
                price=auction.current_price() + idx
            )
            print(
                'Created bid for {} on auction {}'.format(
                  bid.price, auction.title
                )
            )
            time.sleep(2)
