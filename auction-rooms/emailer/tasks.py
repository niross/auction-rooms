from celery.task import task

from . import emails


@task
def provider_auction_finished(**kwargs):
    emails.ProviderAuctionFinished(**kwargs).send()


@task
def guest_auction_won(**kwargs):
    emails.GuestAuctionWon(**kwargs).send()


@task
def guest_auction_lost(**kwargs):
    emails.GuestAuctionLost(**kwargs).send()


@task
def favourite_auction_relisted_email(**kwargs):
    emails.FavouritedAuctionReListedEmail(**kwargs).send()
