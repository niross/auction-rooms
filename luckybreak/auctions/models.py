from __future__ import unicode_literals
from datetime import datetime
import os

import pytz

from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.gis.db import models

from luckybreak.common.models import (
    DeletableTimeStampedModel, DeletableTimeStampedManager
)
from luckybreak.experiences.models import Experience
from luckybreak.users.models import User
from luckybreak.currencies.models import Currency


class AuctionManager(DeletableTimeStampedManager):
    def create_auction(self, experience, check_in, check_out,
                       starting_price, reserve_price, end_date):
        """
        Create an auction from an experience
        """
        auction = self.create(
            experience=experience,
            title=experience.title,
            description=experience.description,
            location=experience.location,
            coords=experience.coords,
            terms=experience.terms,
            pax_adults=experience.pax_adults,
            pax_children=experience.pax_children,
            currency=experience.currency,
            check_in=check_in,
            check_out=check_out,
            starting_price=starting_price,
            reserve_price=reserve_price,
            end_date=end_date
        )

        # Copy the experience images over
        for experience_image in auction.experience.images.all():
            image_copy = ContentFile(experience_image.image.read())
            new_path = os.path.join(
                settings.MEDIA_ROOT,
                AuctionImage.image.field.upload_to,
                os.path.basename(experience_image.image.name)
            )
            auction_image = AuctionImage(auction=auction)
            auction_image.image.save(new_path, image_copy)
            auction_image.save()

        # Copy the inclusions over
        for experience_inclusion in auction.experience.inclusions.all():
            AuctionInclusion.objects.create(
                auction=auction,
                name=experience_inclusion.name
            )

        # Copy the exclusions over
        for experience_exclusion in auction.experience.exclusions.all():
            AuctionExclusion.objects.create(
                auction=auction,
                name=experience_exclusion.name
            )

        return auction


class Auction(DeletableTimeStampedModel):
    experience = models.ForeignKey(Experience, related_name='auctions')

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    coords = models.PointField()
    terms = models.TextField(null=True, blank=True)
    pax_adults = models.PositiveSmallIntegerField(default=2)
    pax_children = models.PositiveSmallIntegerField(default=0)
    currency = models.ForeignKey(Currency, default=settings.DEFAULT_CURRENCY_ID)

    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateTimeField()

    view_count = models.PositiveIntegerField(default=0)
    search_appearance_count = models.PositiveIntegerField(default=0)

    objects = AuctionManager()

    def __unicode__(self):
        return '{}, {}, ending {}'.format(
            self.title,
            self.formatted_current_price(),
            self.end_date
        )

    def is_live(self):
        """
        Return whether the auction is still biddable
        """
        return self.end_date > datetime.utcnow().replace(tzinfo=pytz.utc)

    def status(self):
        if self.is_live():
            return 'Live'
        return 'Complete'

    def highest_bid(self):
        if self.bids.count() > 0:
            return self.bids().order_by('-price').first()
        return None

    def current_price(self):
        bid = self.highest_bid()
        if bid is not None:
            return bid.price
        return self.starting_price

    def formatted_current_price(self):
        return '{}{}'.format(
            self.currency.symbol,
            self.current_price()
        )


class AuctionImage(models.Model):
    auction = models.ForeignKey(Auction, related_name='images')
    image = models.ImageField(upload_to='auctions/')
    default = models.BooleanField(default=False)

    def __unicode__(self):
        return '{} Image'.format(self.auction.title)

    def __str__(self):
        return self.__unicode__()


class AuctionInclusion(models.Model):
    auction = models.ForeignKey(Auction, related_name='inclusions')
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return 'Includes {}'.format(self.name)

    def __str__(self):
        return self.__unicode__()


class AuctionExclusion(models.Model):
    auction = models.ForeignKey(Auction, related_name='exclusions')
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return 'Excludes {}'.format(self.name)

    def __str__(self):
        return self.__unicode__()


class Bid(DeletableTimeStampedModel):
    auction = models.ForeignKey(Auction, related_name='bids')
    user = models.ForeignKey(User, related_name='bids')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('-price',)

    def __unicode__(self):
        return '{} bid on {} from {}'.format(
            self.formatted_price(),
            self.auction.title,
            self.user.get_full_name()
        )

    def formatted_price(self):
        return '{}{}'.format(
            self.auction.currency.symbol,
            self.price
        )
