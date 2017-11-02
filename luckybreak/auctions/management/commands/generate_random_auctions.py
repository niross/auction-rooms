import random
from datetime import datetime, timedelta

from django.core.management import BaseCommand

from luckybreak.auctions.models import Auction
from luckybreak.experiences.models import Experience


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            type=int,
            help='How many auctions to create',
            default=5
        )

    def handle(self, *args, **kwargs):
        for i in range(0, kwargs['amount']):
            checkin = datetime.now() + timedelta(
                days=random.randint(8, 50),
                hours=random.randint(0, 24)
            )
            auction = Auction.objects.create_auction(
                Experience.objects.all()[
                    random.randint(0, Experience.objects.count() - 1)
                ],
                checkin,
                checkin + timedelta(days=1),
                float(random.randint(12, 99)),
                99999,
                datetime.now() + timedelta(
                    days=random.randint(2, 7),
                    hours=random.randint(0, 24)
                )
            )
            if random.randint(0, 2) == 0:
                auction.featured = True
                auction.save()

        print 'Finished creating {} auctions'.format(kwargs['amount'])
