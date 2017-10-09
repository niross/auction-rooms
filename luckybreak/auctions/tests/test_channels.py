from __future__ import unicode_literals

from channels import Channel, Group
from channels.test import WSClient

from luckybreak.auctions.models import Auction, Bid
from luckybreak.common.tests import BaseChannelTestCase


class ProviderAuctionStreamTestCase(BaseChannelTestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json', 'auctions.json'
    ]

    def setUp(self):
        super(ProviderAuctionStreamTestCase, self).setUp()
        self.client = WSClient()
        self.auction = Auction.objects.get(pk=1)

    def test_unauthenticated(self):
        self.client.send_and_consume(
            'websocket.connect', path='/provider/auctions/1/stream/',
            check_accept=False
        )
        self.assertEqual(self.client.receive(), {'accept': False})

    def test_guest(self):
        self.client.force_login(self.guest)
        self.client.send_and_consume(
            'websocket.connect', path='/provider/auctions/1/stream/',
            check_accept=False
        )
        self.assertEqual(self.client.receive(), {'accept': False})

    def test_provider(self):
        self.client.force_login(self.provider)
        self.client.send_and_consume(
            'websocket.connect', path='/provider/auctions/1/stream/',
        )

        bid = Bid.objects.create(
            auction=self.auction,
            user=self.guest,
            price=self.auction.current_price() + 1,
        )
        message = self.client.receive()
        self.assertEqual(message['id'], bid.id)