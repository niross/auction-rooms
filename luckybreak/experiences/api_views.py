# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from . import models
from . import serializers

log = logging.getLogger(__name__)


class ExperienceViewSet(viewsets.ModelViewSet):
    """
    API endpooint for listing, creating and editing Experiences
    """
    queryset = models.Experience.objects.live()
    serializer_class = serializers.ExperienceReadSerializer
