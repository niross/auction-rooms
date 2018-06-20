# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging

from rest_framework import status, mixins
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auctioneer.common.permissions import IsProviderPerm
from auctioneer.users.models import User
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


class FavouriteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating/deleting user favourites
    """
    queryset = models.Favourite.objects.live()
    serializer_class = serializers.FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer)
        )

    def destroy(self, request, *args, **kwargs):
        self.get_queryset().filter(auction__id=kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublicAuctionViewSet(viewsets.GenericViewSet):
    """
    API endpoint for creating auctions
    """
    queryset = models.Auction.objects.filter(deleted=False)
    serializer_class = serializers.BidCreateSerializer
    permission_classes = [IsAuthenticated]

    @detail_route(methods=['POST'])
    def bid(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = self.request.user.id
        data['auction'] = self.get_object().id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

