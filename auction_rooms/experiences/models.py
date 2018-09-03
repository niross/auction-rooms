from __future__ import unicode_literals

from django.conf import settings
from django.contrib.gis.db import models

from auction_rooms.users.models import User
from auction_rooms.common.models import DeletableTimeStampedModel
from auction_rooms.currencies.models import Currency


class Experience(DeletableTimeStampedModel):
    user = models.ForeignKey(
        User,
        related_name='experiences',
        on_delete=models.DO_NOTHING
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    coords = models.PointField()
    terms = models.TextField(null=True, blank=True)
    pax_adults = models.PositiveSmallIntegerField(default=2)
    pax_children = models.PositiveSmallIntegerField(default=0)
    currency = models.ForeignKey(
        Currency,
        default=settings.DEFAULT_CURRENCY_ID,
        on_delete=models.DO_NOTHING
    )
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    def sold_auctions(self):
        from auction_rooms.auctions.models import Auction
        return self.auctions.filter(status=Auction.STATUS_FINISHED_SOLD)

    def live_auctions(self):
        from auction_rooms.auctions.models import Auction
        return self.auctions.filter(status=Auction.STATUS_LIVE)


class ExperienceImage(models.Model):
    experience = models.ForeignKey(
        Experience,
        related_name='images',
        on_delete=models.DO_NOTHING
    )
    image = models.ImageField(upload_to='experiences/')
    default = models.BooleanField(default=False)

    def __unicode__(self):
        return '{} Image'.format(self.experience.title)

    def __str__(self):
        return self.__unicode__()


class ExperienceInclusion(models.Model):
    experience = models.ForeignKey(
        Experience,
        related_name='inclusions',
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return 'Includes {}'.format(self.name)

    def __str__(self):
        return self.__unicode__()


class ExperienceExclusion(models.Model):
    experience = models.ForeignKey(
        Experience,
        related_name='exclusions',
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return 'Excludes {}'.format(self.name)

    def __str__(self):
        return self.__unicode__()
