# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from model_utils.models import TimeStampedModel


class EmailLog(TimeStampedModel):
    recipient = models.EmailField()
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return '{} email sent to {}'.format(
            self.name,
            self.recipient
        )
