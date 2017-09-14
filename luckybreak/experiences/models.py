from __future__ import unicode_literals

from django.conf import settings
from django.contrib.gis.db import models

from luckybreak.users.models import User
from luckybreak.common.models import DeletableTimeStampedModel
from luckybreak.currencies.models import Currency


class Experience(DeletableTimeStampedModel):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    coords = models.PointField()
    terms = models.TextField(null=True, blank=True)
    pax_adults = models.PositiveSmallIntegerField(default=2)
    pax_children = models.PositiveSmallIntegerField(default=0)
    currency = models.ForeignKey(Currency, default=settings.DEFAULT_CURRENCY_ID)
    banner_image = models.ImageField(upload_to='experiences/')

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()


class ExperienceImage(models.Model):
    experience = models.ForeignKey(Experience, related_name='images')
    image = models.ImageField(upload_to='experiences/')
    default = models.BooleanField(default=False)

    def __unicode__(self):
        return '{} Image'.format(self.experience.title)

    def __str__(self):
        return self.__unicode__()


class ExperienceInclusion(models.Model):
    experience = models.ForeignKey(Experience, related_name='inclusions')
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return 'Includes {}'.format(self.name)

    def __str__(self):
        return self.__unicode__()


class ExperienceExclusion(models.Model):
    experience = models.ForeignKey(Experience, related_name='exclusions')
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return 'Excludes {}'.format(self.name)

    def __str__(self):
        return self.__unicode__()
