from datetime import datetime, timedelta

from django.urls import reverse

from rest_framework import status

from luckybreak.common.tests import BaseAPITestCase
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
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(models.Auction.objects.all().count(), count + 3)
