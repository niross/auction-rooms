from auction_rooms.common.tests import BaseTestCase


class ProviderLiveAuctionsTestCase(BaseTestCase):
    def test_unauthenticated_get(self):
        self.get('auctions:provider-live-auctions')
        self.response_403()

    def test_guest_get(self):
        self.client.force_login(self.guest)
        self.get('auctions:provider-live-auctions')
        self.response_403()

    def test_provider_get(self):
        self.client.force_login(self.provider)
        self.get('auctions:provider-live-auctions')
        self.response_200()


class ProviderFinishedAuctionsTestCase(BaseTestCase):
    def test_unauthenticated_get(self):
        self.get('auctions:provider-finished-auctions')
        self.response_403()

    def test_guest_get(self):
        self.client.force_login(self.guest)
        self.get('auctions:provider-finished-auctions')
        self.response_403()

    def test_provider_get(self):
        self.client.force_login(self.provider)
        self.get('auctions:provider-finished-auctions')
        self.response_200()


class ProviderAuctionDetailTestCase(BaseTestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json', 'auctions.json'
    ]

    def test_unauthenticated_get(self):
        self.get('auctions:provider-auction', pk=1)
        self.response_403()

    def test_guest_get(self):
        self.client.force_login(self.guest)
        self.get('auctions:provider-auction', pk=1)
        self.response_403()

    def test_provider_get(self):
        self.client.force_login(self.provider)
        self.get('auctions:provider-auction', pk=1)
        self.response_200()


class FavouritesTestCase(BaseTestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json', 'auctions.json'
    ]

    def test_unauthenticated_get(self):
        self.get('auctions:favourites')
        self.response_302()

    def test_guest_get(self):
        self.client.force_login(self.guest)
        self.get('auctions:favourites')
        self.response_200()

    def test_provider_get(self):
        self.client.force_login(self.provider)
        self.get('auctions:favourites')
        self.response_200()


class GuestWonAuctionsTestCase(BaseTestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json', 'auctions.json'
    ]

    def test_unauthenticated_get(self):
        self.get('auctions:won-auctions')
        self.response_302()

    def test_guest_get(self):
        self.client.force_login(self.guest)
        self.get('auctions:won-auctions')
        self.response_200()

    def test_provider_get(self):
        self.client.force_login(self.provider)
        self.get('auctions:won-auctions')
        self.response_200()


class GuestBidsTestCase(BaseTestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json', 'auctions.json'
    ]

    def test_unauthenticated_get(self):
        self.get('auctions:bids')
        self.response_302()

    def test_guest_get(self):
        self.client.force_login(self.guest)
        self.get('auctions:bids')
        self.response_200()

    def test_provider_get(self):
        self.client.force_login(self.provider)
        self.get('auctions:bids')
        self.response_200()
