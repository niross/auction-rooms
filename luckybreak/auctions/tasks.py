import logging
from datetime import datetime

from celery.task import task
from django.db.models import F

from luckybreak.auctions.models import Auction

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
        print('Marking auction \'%s\' as complete', auction.id)
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
