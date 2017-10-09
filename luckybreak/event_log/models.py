# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.postgres.fields import JSONField


class EventLogManager(models.Manager):
    def log_experience_created(self, user, experience):
        return self.create(
            user=user,
            type=EventLog.EVENT_TYPE_CREATE_EXPERIENCE,
            content_object=experience
        )

    def log_auction_created(self, user, auction):
        return self.create(
            user=user,
            type=EventLog.EVENT_TYPE_CREATE_AUCTION,
            content_object=auction
        )

    def log_bid_placed(self, user, bid):
        return self.create(
            user=user,
            type=EventLog.EVENT_TYPE_BID_PLACED,
            content_object=bid
        )

    def log_auction_ended(self, user, auction):
        return self.create(
            user=user,
            type=EventLog.EVENT_TYPE_AUCTION_ENDED,
            content_object=auction
        )


class EventLog(TimeStampedModel):
    EVENT_TYPE_CREATE_EXPERIENCE = 1
    EVENT_TYPE_CREATE_AUCTION = 2
    EVENT_TYPE_BID_PLACED = 3
    EVENT_TYPE_AUCTION_ENDED = 4

    _EVENT_TYPE_CHOICES = (
        (EVENT_TYPE_CREATE_EXPERIENCE, 'A new experience was created'),
        (EVENT_TYPE_CREATE_AUCTION, 'A new auction was created'),
        (EVENT_TYPE_BID_PLACED, 'A bid was placed on an auction'),
        (EVENT_TYPE_AUCTION_ENDED, 'Auction finished'),
    )
    user = models.ForeignKey('users.User', related_name='events')
    type = models.IntegerField(choices=_EVENT_TYPE_CHOICES)
    data = JSONField(null=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True
    )
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = EventLogManager()

    class Meta:
        ordering = ('-created',)

    def get_log_message(self):
        if self.type == self.EVENT_TYPE_CREATE_EXPERIENCE:
            return 'A new experience, <span class="experience-app" ' \
               'data-modal-id="edit-{id}-modal" ' \
               'data-button-id="edit-{id}-button" ' \
               'data-button-text="{title}" ' \
               'data-button-flat="true" ' \
               'data-experience-id="{id}" ' \
               '></span>, was created.'.format(
                    id=self.content_object.id,
                    title=self.content_object.title
                )

        if self.type == self.EVENT_TYPE_CREATE_AUCTION:
            return 'A new auction, <a href="{}">{}</a>, was created.'.format(
                self.content_object.get_provider_absolute_url(),
                self.content_object.title
            )

        if self.type == self.EVENT_TYPE_BID_PLACED:
            return 'A bid for {} was received on auction, ' \
               '<a href="{}">{}</a>.'.format(
                    self.content_object.auction.formatted_current_price(),
                    self.content_object.auction.get_provider_absolute_url(),
                    self.content_object.auction.title
                )

        if self.type == self.EVENT_TYPE_AUCTION_ENDED:
            return 'Auction <a href="{}">{}</a> finished.'.format(
                    self.content_object.get_provider_absolute_url(),
                    self.content_object.title
            )

