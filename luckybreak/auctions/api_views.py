# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging

from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response

from luckybreak.common.permissions import IsProviderPerm
from . import models
from . import serializers

log = logging.getLogger(__name__)


class ProviderAuctionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint for creating auctions
    """
    queryset = models.Auction.objects.live()
    serializer_class = serializers.AuctionCreateSerializer
    permission_classes = [IsProviderPerm]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auction = serializer.save()

        serializer = serializers.AuctionReadSerializer(auction, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer)
        )
