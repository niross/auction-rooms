from __future__ import unicode_literals

from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=3, unique=True)
    symbol = models.CharField(max_length=3)
    html_code = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()
