# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from luckybreak.common.permissions import IsProviderPerm
from . import models
from . import serializers

log = logging.getLogger(__name__)


class ProviderAuctionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating auctions
    """
    queryset = models.Auction.objects.filter(deleted=False)
    serializer_class = serializers.AuctionReadSerializer
    permission_classes = [IsProviderPerm]

    def get_queryset(self):
        return self.queryset.filter(experience__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = serializers.AuctionCreateSerializer(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        auction = serializer.save()

        serializer = serializers.AuctionReadSerializer(auction, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer)
        )
