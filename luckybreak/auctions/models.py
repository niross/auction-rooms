from __future__ import unicode_literals
from datetime import datetime, timedelta
import os

import pytz
from channels import Group

from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.gis.db import models
from django.urls import reverse
from django_extensions.db.fields import ShortUUIDField

from luckybreak.common.models import DeletableTimeStampedModel
from luckybreak.experiences.models import Experience
from luckybreak.users.models import User
from luckybreak.currencies.models import Currency


class AuctionQuerySet(models.QuerySet):
    def live(self):
        """
        Returns auctions that have not yet finished
        """
        return self.filter(
            deleted=False,
            end_date__gt=datetime.utcnow()
        )

    def finished(self):
        """
        Returns auctions that have finished
        """
        return self.filter(
            deleted=False,
            end_date__lte=datetime.utcnow()
        )

    def sold(self):
        return self.filter(
            deleted=False,
            status=Auction.STATUS_FINISHED_SOLD
        )


class AuctionManager(models.Manager):
    def get_queryset(self):
        return AuctionQuerySet(self.model, using=self._db)

    def create_auction(self, experience, check_in, check_out, # pylint: disable=too-many-arguments
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
                AuctionImage.image.field.upload_to,  # pylint: disable=no-member
                os.path.basename(experience_image.image.name)
            )
            auction_image = AuctionImage(auction=auction)
            auction_image.image.save(new_path, image_copy, True)
            auction_image.image.name = os.path.join(AuctionImage.image.field.upload_to, os.path.basename(experience_image.image.name))
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

    def live(self):
        """
        Returns auctions that have not yet finished
        """
        return self.get_queryset().live()

    def finished(self):
        """
        Returns auctions that have finished
        """
        return self.get_queryset().finished()

    def sold(self):
        """
        Returns auctions that have finished
        """
        return self.get_queryset().sold()


class Auction(DeletableTimeStampedModel):
    STATUS_LIVE = 1
    STATUS_FINISHED_SOLD = 2
    STATUS_FINISHED_UNSOLD = 3
    _STATUS_CHOICES = (
        (STATUS_LIVE, 'Live'),
        (STATUS_FINISHED_SOLD, 'Finished Sold'),
        (STATUS_FINISHED_UNSOLD, 'Finished Unsold'),
    )
    status = models.IntegerField(
        choices=_STATUS_CHOICES,
        default=STATUS_LIVE
    )
    experience = models.ForeignKey(
        Experience,
        related_name='auctions',
        help_text='The experience this auction was created from'
    )
    title = models.CharField(
        max_length=255,
        help_text='Title of the experience being auctioned'
    )
    description = models.TextField(
        help_text='Description of the experience being auctioned'
    )
    location = models.CharField(
        max_length=255,
        help_text='Location name of the experience'
    )
    coords = models.PointField(
        help_text='Location coordinates of the experience'
    )
    terms = models.TextField(
        null=True,
        blank=True,
        help_text='Terms and conditions for the auction/experience'
    )
    pax_adults = models.PositiveSmallIntegerField(
        default=2,
        help_text='Number of adults accepted as part of the experience'
    )
    pax_children = models.PositiveSmallIntegerField(
        default=0,
        help_text='Number of children accepted as part of the experience'
    )
    currency = models.ForeignKey(
        Currency,
        default=settings.DEFAULT_CURRENCY_ID,
        help_text='The date and time the experience starts'
    )
    check_in = models.DateTimeField(
        help_text='The date and time the experience starts'
    )
    check_out = models.DateTimeField(
        help_text='The date and time the experience ends'
    )
    starting_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='The initial price for the auction when it goes live'
    )
    reserve_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='The minimum price that will be accpeted to win this auction'
    )
    end_date = models.DateTimeField(
        help_text='The date and time the auction finishes'
    )
    view_count = models.PositiveIntegerField(
        default=0,
        help_text='The number of times auction details have been viewed'
    )
    search_appearance_count = models.PositiveIntegerField(
        default=0,
        help_text='The number of times this auction has ' \
                  'appeared in search results or on the homepage'
    )
    featured = models.BooleanField(
        default=False,
        help_text='Set to true to show this auction in ' \
                  'the featured section on the homepage'
    )
    uuid = ShortUUIDField()

    objects = AuctionManager()

    def __unicode__(self):
        return '{}, {}, ending {}'.format(
            self.title,
            self.formatted_current_price(),
            self.end_date
        )

    def get_provider_absolute_url(self):
        return reverse('auctions:provider-auction', args=(self.id,))

    def get_guest_absolute_url(self):
        return reverse('auctions:public-auction', args=(self.id,))

    def get_guest_confirmation_url(self):
        return '{}#confirm-{}'.format(
            reverse('auctions:won-auctions'),
            self.id
        )

    def is_live(self):
        """
        Return whether the auction is still biddable
        """
        return self.end_date > datetime.utcnow().replace(tzinfo=pytz.utc)

    def is_finished(self):
        """
        Return whether the auction is still biddable
        """
        return self.end_date <= datetime.utcnow().replace(tzinfo=pytz.utc)

    def was_won(self):
        return self.is_finished() and self.current_price() > self.reserve_price

    def highest_bid(self):
        if self.bids.count() > 0:
            return self.bids.order_by('-price').first()
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

    def formatted_reserve_price(self):
        return '{}{}'.format(
            self.currency.symbol,
            self.reserve_price
        )

    def formatted_starting_price(self):
        return '{}{}'.format(
            self.currency.symbol,
            self.starting_price
        )

    def get_default_image(self):
        if self.images.filter(default=True).exists():
            return self.images.filter(default=True).first()
        return self.images.first()

    @property
    def provider_websocket_group(self):
        """
        Return the channel name that a provider should subscribe to
        when viewing a live auction.
        :return:
        """
        return Group('provider-auction-{}'.format(self.id))

    def send_provider_message(self, message):
        self.provider_websocket_group.send(message)

    @property
    def public_websocket_group(self):
        """
        Return the channel name that a provider should subscribe to
        when viewing a live public auction.
        :return:
        """
        return Group('public-auction-{}'.format(self.id))

    def send_public_message(self, message):
        self.public_websocket_group.send(message)

    def mark_complete(self):
        from luckybreak.auctions.signals import auction_completed

        if self.bids.count() == 0 or self.current_price() < self.reserve_price:
            # Auction did not sell
            self.status = self.STATUS_FINISHED_UNSOLD
        else:
            # Auction sold
            self.status = self.STATUS_FINISHED_SOLD
        self.save()
        auction_completed.send(sender=self.__class__, auction=self)

    def is_ending(self):
        now = datetime.utcnow().replace(tzinfo=pytz.utc)
        return self.end_date < now + timedelta(hours=24)

    def pretty_duration(self):
        days = (self.check_out.date() - self.check_in.date()).days
        return '{} Night{}'.format(days, 's' if days > 1 else '')


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
        unique_together = ('auction', 'price')
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


class Favourite(DeletableTimeStampedModel):
    auction = models.ForeignKey(Auction, related_name='favourites')
    user = models.ForeignKey(User, related_name='favourites')
