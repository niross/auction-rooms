from django.core.management import BaseCommand

from auction_rooms.auctions.tasks import complete_auctions


class Command(BaseCommand):
    help = 'Run the auction completer to find and complete ' \
           'any auctions that have finished'

    def handle(self, *args, **kwargs):
        complete_auctions()
