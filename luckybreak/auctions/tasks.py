import logging
from datetime import datetime, timedelta

from celery.task import task
from dateutil.relativedelta import relativedelta
from django.db.models import F, Q

from luckybreak.auctions.models import Auction, Favourite
from luckybreak.emailer.tasks import favourite_auction_relisted_email

log = logging.getLogger(__name__)


@task
def complete_auctions():
    """
    Find any completed auctions and mark them as complete
    :return:
    """
    print('Running complete auctions task')
    log.debug('Running complete auctions task')

    to_complete = Auction.objects.filter(
        deleted=False,
        end_date__lte=datetime.utcnow(),
        status=Auction.STATUS_LIVE
    )
    for auction in to_complete:
        print('Marking auction {} as complete'.format(auction.id))
        log.debug('Marking auction \'%s\' as complete', auction.id)
        auction.mark_complete()


@task
def increment_search_appearance_count(auction_ids):
    """
    Add 1 to the search_appearance_count field for
    all auction ids provided

    :param auction_ids:
    :return:
    """
    Auction.objects.filter(id__in=auction_ids).update(
        search_appearance_count=F('search_appearance_count') + 1
    )


@task
def increment_view_count(auction_id):
    """
    Add 1 to the view_count field for the provided auction id

    :param auction_id:
    :return:
    """
    Auction.objects.filter(id=auction_id).update(
        view_count=F('view_count') + 1
    )


@task
def send_new_listing_notifications(auction_id):
    """
    Send a new listing email out to any users who have favourited, but not won,
    an auction with the same experience as the provided auction.

    The favourite auction:
      1. Must be finished
      2. Cannot have been won by the user
      3. Must have finished in the last 3 months

    Users:
      1. Must not have won the favourited auction
      2. Have not received a new listing email about the favourited auction
      3. Have not received a new listing email (about any experience) today
    :param auction_id:
    :return:
    """
    auction = Auction.objects.get(pk=auction_id)

    # Favourites that are for the same experience,
    # have finished and have not been sent a new listing email
    favourites = Favourite.objects.filter(
        auction__experience=auction.experience,
        auction__deleted=False,
        auction__end_date__range=(
            datetime.utcnow() - relativedelta(months=6),
            datetime.utcnow()
        ),
        new_listing_sent=False,
    )

    for favourite in favourites:
        # Ensure the user didn't win the favourited auction
        winning_bid = favourite.auction.highest_bid()
        if winning_bid is None or winning_bid.user != favourite.user:
            # Ensure the user hasn't received any new listing emails today
            emails = favourite.user.emails().filter(
                created__date=datetime.utcnow().date(),
                name='Favourited Auction Relisted'
            )
            if emails.count() == 0:
                favourite_auction_relisted_email(
                    recipient_id=favourite.user.id,
                    auction_id=auction.id,
                    favourite_id=favourite.id
                )
                favourite.new_listing_sent = True
                favourite.save()
