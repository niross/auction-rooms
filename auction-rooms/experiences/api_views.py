# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import parser_classes

from auctioneer.common.permissions import IsProviderPerm
from . import models
from . import serializers

log = logging.getLogger(__name__)


class ExperienceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, creating and editing Experiences
    """
    queryset = models.Experience.objects.live()
    serializer_class = serializers.ExperienceReadSerializer
    permission_classes = [IsProviderPerm]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @parser_classes([FormParser, MultiPartParser])
    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        serializer = serializers.ExperienceCreateSerializer(
            data=data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        experience = serializer.save()

        serializer = self.get_serializer(experience)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer)
        )

    @parser_classes([FormParser, MultiPartParser])
    def update(self, request, *args, **kwargs):
        data = request.data
        serializer = serializers.ExperienceUpdateSerializer(
            self.get_object(),
            data=data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        experience = serializer.save()

        serializer = self.get_serializer(experience)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=self.get_success_headers(serializer)
        )
