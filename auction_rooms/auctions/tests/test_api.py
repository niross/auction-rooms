# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime, timedelta

import pytz
from django.urls import reverse

from rest_framework import status

from auction_rooms.auctions.models import Favourite, Auction, Bid
from auction_rooms.common.tests import BaseAPITestCase
from .. import models


class ProviderAuctionAPITestCase(BaseAPITestCase):
    fixtures = ['users.json', 'currencies.json', 'experiences.json']

    def test_unauthed_create_auction(self):
        """
        Unauthenticated users cannot create auctions
        """
        response = self.client.post(
            reverse('auction-api:provider-auction-list'),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_guest_create_auction(self):
        """
        Guests cannot create auctions
        """
        self.client.force_authenticate(user=self.guest)
        response = self.client.post(
            reverse('auction-api:provider-auction-list'),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_check_in_before_check_out(self):
        self.client.force_authenticate(user=self.provider)
        experience = self.provider.experiences.last()
        response = self.client.post(
            reverse('auction-api:provider-auction-list'),
            data={
                'experience': experience.id,
                'check_in': '2029-01-01 11:00:00',
                'check_out': '2029-01-01 10:55:00',
                'starting_price': 99.99,
                'reserve_price': 199.99,
                'lots': 3,
                'duration_days': 3,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'check_out': ['Check out must be after check in']}
        )

    def test_check_in_before_auction_end(self):
        self.client.force_authenticate(user=self.provider)
        experience = self.provider.experiences.last()
        checkin = datetime.now() + timedelta(days=5)
        checkout = checkin + timedelta(days=1)

        response = self.client.post(
            reverse('auction-api:provider-auction-list'),
            data={
                'experience': experience.id,
                'check_in': checkin.strftime('%Y-%m-%d %H:%M:%S'),
                'check_out': checkout.strftime('%Y-%m-%d %H:%M:%S'),
                'starting_price': 99.99,
                'reserve_price': 199.99,
                'lots': 3,
                'duration_days': 7,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'check_in': ['Check in cannot be before auction end date']}
        )

    def test_create_auction(self):
        events = self.provider.events.count()
        self.client.force_authenticate(user=self.provider)
        experience = self.provider.experiences.last()
        count = models.Auction.objects.all().count()
        checkin = datetime.now() + timedelta(days=5)
        checkout = checkin + timedelta(days=1)

        response = self.client.post(
            reverse('auction-api:provider-auction-list'),
            data={
                'experience': experience.id,
                'check_in': checkin.strftime('%Y-%m-%d %H:%M:%S'),
                'check_out': checkout.strftime('%Y-%m-%d %H:%M:%S'),
                'starting_price': 99.99,
                'reserve_price': 199.99,
                'lots': 3,
                'duration_days': 3,
            },
            format='json',
            headers={
                'Content-Type': "application/json; charset=utf-8"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # DRF test client fails to parse json as it's expecting ascii
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 3)
        self.assertEqual(models.Auction.objects.all().count(), count + 3)
        self.assertEqual(self.provider.events.count(), events + 3)


class AuctionFavouriteAPITestCase(BaseAPITestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json',
        'auctions.json',
    ]

    def test_unauthed_favourite(self):
        """
        Unauthenticated users cannot favourite auctions
        """
        response = self.client.post(
            reverse('auction-api:favourites-detail', kwargs={'pk': 1}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthed_unfavourite(self):
        """
        Unauthenticated users cannot unfavourite auctions
        """
        response = self.client.delete(
            reverse('auction-api:favourites-detail', kwargs={'pk': 1}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_guest_favourite(self):
        """
        Guests can favourite auctions
        """
        self.client.force_authenticate(self.guest)
        response = self.client.post(
            reverse('auction-api:favourites-list'),
            data={'auction': 1}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_guest_unfavourite(self):
        """
        Guests can unfavourite auctions
        """
        self.client.force_authenticate(self.guest)
        Favourite.objects.create(
            auction=Auction.objects.get(pk=1),
            user=self.guest
        )
        response = self.client.delete(
            reverse('auction-api:favourites-detail', kwargs={'pk': 1}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.guest.favourites.count(), 0)

    def test_provider_favourite(self):
        """
        providers can favourite auctions
        """
        self.client.force_authenticate(self.provider)
        response = self.client.post(
            reverse('auction-api:favourites-list'),
            data={'auction': 1}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_provider_unfavourite(self):
        """
        providers can unfavourite auctions
        """
        self.client.force_authenticate(self.provider)
        Favourite.objects.create(
            auction=Auction.objects.get(pk=1),
            user=self.provider
        )
        response = self.client.delete(
            reverse('auction-api:favourites-detail', kwargs={'pk': 1}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.provider.favourites.count(), 0)


class PublicAuctionAPITestCase(BaseAPITestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json',
        'auctions.json'
    ]

    def test_unauthed_bid(self):
        response = self.client.post(
            reverse('auction-api:public-auction-bid', kwargs={'pk': 1}),
            data={'price': 22}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bid_on_own_auction(self):
        self.client.force_authenticate(self.provider)
        response = self.client.post(
            reverse('auction-api:public-auction-bid', kwargs={'pk': 1}),
            data={'price': 35}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'price': ['You cannot bid on your own auctions']}
        )

    def test_bid_too_low(self):
        self.client.force_authenticate(self.guest)
        response = self.client.post(
            reverse('auction-api:public-auction-bid', kwargs={'pk': 1}),
            data={'price': 33}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'price': ['Please enter a bid of 34.00 or over']}
        )

    def test_already_highest_bidder(self):
        self.client.force_authenticate(self.guest)
        Bid.objects.create(
            user=self.guest,
            auction=Auction.objects.get(pk=1),
            price=99
        )
        response = self.client.post(
            reverse('auction-api:public-auction-bid', kwargs={'pk': 1}),
            data={'price': 100}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'price': ['You are already the highest bidder!']}
        )

    def test_bid_on_finished_auction(self):
        self.client.force_authenticate(self.guest)
        auction = Auction.objects.get(pk=1)
        auction.end_date = datetime.now(pytz.UTC) - timedelta(minutes=1)
        auction.save()
        response = self.client.post(
            reverse('auction-api:public-auction-bid', kwargs={'pk': 1}),
            data={'price': 100}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'price': ['This auction has finished']}
        )

    def test_bid(self):
        self.client.force_authenticate(self.guest)
        bids = Auction.objects.get(pk=1).bids.count()
        response = self.client.post(
            reverse('auction-api:public-auction-bid', kwargs={'pk': 1}),
            data={'price': 34}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        auction = Auction.objects.get(pk=1)
        self.assertEqual(auction.bids.count(), bids + 1)
        self.assertEqual(auction.current_price(), 34.0)
