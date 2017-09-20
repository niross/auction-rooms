from luckybreak.common.tests import BaseTestCase


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
